from datetime import datetime
from multiprocessing.pool import ThreadPool

import gym
import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
from tqdm import tqdm

from envs.remote.client import RemoteEnv
from config import env_config


def get_rewards(states, rewards):
    voltages, reactive_powers = tf.split(states, 2, axis=1)
    ret = tf.TensorArray(tf.float32, size=states.shape[0])
    ret = ret.write(0, rewards[0])

    for t in range(1, len(states)):
        if tf.reduce_all(tf.abs(voltages[t] - 1) < env_config['voltage_threshold'] * 1.023) and \
                tf.reduce_all(tf.abs(reactive_powers[t:t+env_config['window_size'], :] - reactive_powers[t, :]) < env_config['change_threshold']):
            ret = ret.write(t, 1)
        else:
            ret = ret.write(t, 0)

    return ret.stack()


def get_single_trajectory(env, actor):
    """
    Get the experiences from the environment.
    """

    states = []
    actions = []
    scaled_actions = []
    rewards = []
    next_states = []
    dones = []

    observation = env.reset()
    done = False

    while not done:
        logits = actor(np.array([observation]))
        distribution = get_distribution(logits)

        action = distribution.sample()[0]
        prob = distribution.prob(action)[0]

        scaled_action = tf.sigmoid(action) * (env.action_space.high - env.action_space.low) + env.action_space.low

        # action = tf.constant([-2, 1.2, 1.4, -1.7])
        # scaled_action = action
        # prob = tf.constant(1.0)

        new_obs, reward, done, info = env.step(scaled_action)

        states.append(observation)
        actions.append(action)
        scaled_actions.append(scaled_action)
        rewards.append(reward)
        next_states.append(new_obs)
        dones.append(done)

        observation = new_obs

    rewards = get_rewards(np.array(states), np.array(rewards))
    convergence_time = np.where(rewards == 1)[0]
    if len(convergence_time) > 0:
        convergence_time = convergence_time[0]
        print(f'Converged at step {convergence_time}')
    else:
        convergence_time = None

    return dict(
        states=np.array(states)[:convergence_time],
        actions=np.array(actions)[:convergence_time],
        scaled_actions=np.array(scaled_actions)[:convergence_time],
        rewards=rewards[:convergence_time],
        next_states=np.array(next_states)[:convergence_time],
        dones=np.array(dones)[:convergence_time],
    )


def create_critic(env: gym.Env):
    state_dim = env.observation_space.sample().shape

    inputs = tf.keras.layers.Input(shape=state_dim)
    dense = tf.keras.layers.Dense(64, activation='relu')(inputs)
    dense = tf.keras.layers.Dense(64, activation='relu')(dense)
    output = tf.keras.layers.Dense(1, activation='linear')(dense)

    model = tf.keras.Model(inputs=inputs, outputs=output)

    return model


def create_actor(env: gym.Env):

    if env.action_space.__class__.__name__ == 'Box':
        action_dim = env.action_space.sample().shape[0]
    else:
        raise NotImplementedError(f'Action space of {env.action_space.__class__.__name__} not implemented')

    state_dim = env.observation_space.sample().shape

    inputs = tf.keras.layers.Input(state_dim)
    dense = tf.keras.layers.Dense(64, activation='relu')(inputs)
    dense = tf.keras.layers.Dense(64, activation='relu')(dense)
    output = tf.keras.layers.Dense(action_dim * 2, activation='linear')(dense)

    model = tf.keras.Model(inputs=inputs, outputs=output)

    return model


def calculate_gae(rewards, state_vals, next_state_vals, dones, gamma, lam):
    """
    Calculate the advantage function.
    """
    gae = 0
    gae_list = tf.TensorArray(tf.float32, size=rewards.shape[0])
    for i in reversed(range(len(rewards))):
        delta = rewards[i] + gamma * next_state_vals[i] * (1 - dones[i]) - state_vals[i]
        gae = delta + gamma * lam * (1 - dones[i]) * gae
        gae_list = gae_list.write(i, gae[0])
    return gae_list.stack()


def train(epoch, optimizer, actor, critic, trajectories,
          gamma: float, lam: float, epsilon: float, beta: float, c_1: float, c_2: float):

    old_distributions = [get_distribution(actor(t['states']) for t in trajectories)]
    old_probs = [old_distributions[t].prob(trajectories[t]['actions']) for t in range(len(trajectories))]

    for it, trajectory, old_distribution, old_prob in enumerate(zip(trajectories, old_distributions, old_probs)):
        it_log = epoch * len(trajectories) + it

        with tf.GradientTape() as actor_tape, tf.GradientTape() as critic_tape:
            state_val = critic(trajectory['states'], training=True)
            next_state_val = critic(trajectory['next_states'], training=True)
            action_logits = actor(trajectory['states'], training=True)

            distribution = get_distribution(action_logits)
            probs = distribution.prob(trajectory['actions'])
            kl = old_distribution.kl_divergence(distribution)
            r_t = probs / old_prob
            gae = calculate_gae(trajectory['rewards'], state_val, next_state_val, trajectory['dones'], gamma, lam)
            entropy = distribution.entropy()

            l_crit = c_1 * tf.reduce_mean(tf.square(trajectory['rewards'] + gamma * next_state_val * (1 - trajectory['dones']) - state_val))
            l_clip = - tf.reduce_mean(tf.math.minimum(tf.clip_by_value(r_t, 1 - epsilon, 1 + epsilon) * gae, r_t * gae))
            l_kl = beta * tf.reduce_mean(kl)
            l_entropy = - c_2 * tf.reduce_mean(entropy)

            surrogate = - l_kl + l_clip + l_entropy - l_crit

        critic_grads = critic_tape.gradient(l_crit, critic.trainable_variables)
        optimizer.apply_gradients(zip(critic_grads, critic.trainable_variables))

        actor_grads = actor_tape.gradient(l_clip, actor.trainable_variables)
        optimizer.apply_gradients(zip(actor_grads, actor.trainable_variables))

        tf.summary.scalar('ppo/state_val', data=tf.reduce_mean(state_val), step=it_log)
        tf.summary.scalar('ppo/l_val', data=l_crit, step=it_log)
        tf.summary.scalar('ppo/l_clip', data=l_clip, step=it_log)
        tf.summary.scalar('ppo/l_kl', data=l_kl, step=it_log)
        tf.summary.scalar('ppo/l_entropy', data=l_entropy, step=it_log)
        tf.summary.scalar('ppo/l_surrogate', data=surrogate, step=it_log)
        tf.summary.scalar('ppo/r_t', data=tf.reduce_mean(r_t), step=it_log)
        tf.summary.scalar('ppo/gae', data=tf.reduce_mean(gae), step=it_log)

        tf.summary.scalar('parameters/epsilon', data=epsilon, step=it_log)
        tf.summary.scalar('parameters/beta', data=beta, step=it_log)
        tf.summary.scalar('parameters/c_1', data=c_1, step=it_log)
        tf.summary.scalar('parameters/c_2', data=c_2, step=it_log)
        tf.summary.scalar('parameters/gamma', data=gamma, step=it_log)
        tf.summary.scalar('parameters/lam', data=lam, step=it_log)
        tf.summary.scalar('parameters/learning_rate', data=optimizer.lr, step=it_log)

        tf.summary.scalar('env/return', data=tf.reduce_sum(trajectory['rewards']), step=it_log)
        tf.summary.scalar('env/epoch_length', data=tf.reduce_mean(len(trajectory['states'])), step=it_log)
        tf.summary.scalar('env/action_mean', data=tf.reduce_mean(distribution.mean()), step=it_log)
        tf.summary.scalar('env/action_std', data=tf.reduce_mean(distribution.stddev()), step=it_log)

        tf.summary.scalar('power_grid/alpha', data=tf.reduce_mean(trajectory['scaled_actions'][:, 0]), step=it_log)
        tf.summary.scalar('power_grid/beta', data=tf.reduce_mean(trajectory['scaled_actions'][:, 1]), step=it_log)
        tf.summary.scalar('power_grid/gamma', data=tf.reduce_mean(trajectory['scaled_actions'][:, 2]), step=it_log)
        tf.summary.scalar('power_grid/c', data=tf.reduce_mean(trajectory['scaled_actions'][:, 3]), step=it_log)

        tf.summary.scalar('power_grid/min_volt', data=tf.reduce_min(tf.split(trajectory['states'], 2, axis=1)[0]), step=it_log)
        tf.summary.scalar('power_grid/max_volt', data=tf.reduce_max(tf.split(trajectory['states'], 2, axis=1)[0]), step=it_log)

        tf.summary.scalar('power_grid/min_reactive', data=tf.reduce_min(tf.split(trajectory['states'], 2, axis=1)[1]), step=it_log)
        tf.summary.scalar('power_grid/max_reactive', data=tf.reduce_max(tf.split(trajectory['states'], 2, axis=1)[1]), step=it_log)


def get_distribution(action_logits):
    means, stds = tf.split(action_logits, 2, axis=1)
    distribution = tfp.distributions.MultivariateNormalDiag(loc=means, scale_diag=stds)
    return distribution


def main(numcpus):

    with ThreadPool(numcpus) as pool:
        envs = pool.starmap(RemoteEnv, [('localhost', 6985, env_config) for _ in range(numcpus)])

    critic = create_critic(envs[0])
    actor = create_actor(envs[0])

    critic.summary()
    actor.summary()

    optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)  # this should depend on the number of training epochs.

    with ThreadPool(processes=numcpus) as tp:

        for epoch in tqdm(range(1000)):
            trajectories = tp.starmap(get_single_trajectory, [(env, actor) for env in envs])
            train(epoch, optimizer, actor, critic, trajectories, gamma=0.99, lam=1, epsilon=0.3, beta=0.02, c_1=0.1,
                  c_2=0.0001)  # c_1 critic, c_2 entropy


if __name__ == '__main__':

    logdir = "logs/tb_logs" + datetime.now().strftime("%Y%m%d-%H%M%S")
    file_writer = tf.summary.create_file_writer(logdir + "/metrics")
    file_writer.set_as_default()

    main(16)