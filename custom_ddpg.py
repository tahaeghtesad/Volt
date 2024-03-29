import random
import threading
from datetime import datetime
from multiprocessing.pool import ThreadPool

import gym
import tensorflow as tf
from tqdm import tqdm

from config import env_config, custom_ddpg_config
from envs.remote.client import RemoteEnv
from util.env_util import get_rewards


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
    noise = OUActionNoise(mean=custom_ddpg_config['OU_mean'] * tf.ones(env.action_space.low.shape[0]),
                          std_deviation=custom_ddpg_config['OU_std'] * tf.ones(env.action_space.low.shape[0]),
                          theta=custom_ddpg_config['OU_theta'],
                          dt=custom_ddpg_config['OU_dt'])
    done = False

    while not done:
        if random.random() < custom_ddpg_config['exploration_probability']:
            action = tf.random.uniform(env.action_space.low.shape)
        else:
            action = actor(tf.convert_to_tensor([observation]))[0] + noise()

        scaled_action = action * (env.action_space.high - env.action_space.low) + env.action_space.low

        new_obs, reward, done, info = env.step(scaled_action)

        states.append(observation)
        actions.append(action)
        scaled_actions.append(scaled_action)
        rewards.append(reward)
        next_states.append(new_obs)
        dones.append(done)

        observation = new_obs

    rewards = get_rewards(env_config, tf.convert_to_tensor(states, dtype=tf.float32),
                          tf.convert_to_tensor(rewards, dtype=tf.float32), dones)

    convergence_time = tf.where(rewards == 1)
    if len(convergence_time) > 0:
        convergence_time = convergence_time[0][0] + 1
        print(f'Converged at step {convergence_time}')
    else:
        convergence_time = None

    return dict(
        states=tf.convert_to_tensor(states, dtype=tf.float32)[:convergence_time],
        actions=tf.convert_to_tensor(actions, dtype=tf.float32)[:convergence_time],
        scaled_actions=tf.convert_to_tensor(scaled_actions, dtype=tf.float32)[:convergence_time],
        rewards=rewards[:convergence_time],
        next_states=tf.convert_to_tensor(next_states, dtype=tf.float32)[:convergence_time],
        dones=tf.cast(tf.convert_to_tensor(dones), dtype=tf.float32)[:convergence_time],
    )


class OUActionNoise:
    def __init__(self, mean, std_deviation, theta=0.15, dt=1e-2, x_initial=None):
        self.theta = theta
        self.mean = mean
        self.std_dev = std_deviation
        self.dt = dt
        self.x_initial = x_initial
        self.x_prev = None
        self.reset()

    def __call__(self):
        # Formula taken from https://www.wikipedia.org/wiki/Ornstein-Uhlenbeck_process.
        x = (
                self.x_prev
                + self.theta * (self.mean - self.x_prev) * self.dt
                + self.std_dev * tf.math.sqrt(self.dt) * tf.random.normal(self.mean.shape)
        )
        # Store x into x_prev
        # Makes next noise dependent on current one
        self.x_prev = x
        return x

    def reset(self):
        if self.x_initial is not None:
            self.x_prev = self.x_initial
        else:
            self.x_prev = tf.zeros_like(self.mean)


class ExperienceReplayBuffer:
    def __init__(self, buffer_size, batch_size):
        self.buffer_size = buffer_size
        self.batch_size = batch_size
        self.lock = threading.Lock()

        self.buffer = []

    @staticmethod
    def convert_trajectory(trajectory):
        ret = []
        for i in range(len(trajectory['states'])):
            ret.append(dict(
                state=trajectory['states'][i],
                action=trajectory['actions'][i],
                scaled_action=trajectory['scaled_actions'][i],
                reward=trajectory['rewards'][i],
                next_state=trajectory['next_states'][i],
                done=trajectory['dones'][i],
            ))
        return ret

    def add(self, trajectory):
        converted = self.convert_trajectory(trajectory)
        with self.lock:
            remaining_size = self.buffer_size - len(self.buffer)
            to_remove = len(converted) - remaining_size
            if to_remove > 0:
                self.buffer = self.buffer[to_remove:]
            self.buffer.extend(converted)

    def sample(self):
        experiences = random.choices(self.buffer, k=self.batch_size)
        ret = dict(
            states=[],
            actions=[],
            scaled_actions=[],
            rewards=[],
            next_states=[],
            dones=[],
        )

        for e in experiences:
            ret['states'].append(e['state'])
            ret['actions'].append(e['action'])
            ret['scaled_actions'].append(e['scaled_action'])
            ret['rewards'].append(e['reward'])
            ret['next_states'].append(e['next_state'])
            ret['dones'].append(e['done'])

        return {k: tf.convert_to_tensor(v, dtype=tf.float32) for k, v in ret.items()}


def create_critic(env: gym.Env):
    state_dim = env.observation_space.sample().shape
    action_dim = env.action_space.sample().shape

    # State as input
    state_input = tf.keras.layers.Input(shape=(state_dim))
    state_out = tf.keras.layers.Dense(16, activation="relu")(state_input)
    state_out = tf.keras.layers.Dense(32, activation="relu")(state_out)

    # Action as input
    action_input = tf.keras.layers.Input(shape=(action_dim))
    action_out = tf.keras.layers.Dense(32, activation="relu")(action_input)

    # Both are passed through seperate layer before concatenating
    concat = tf.keras.layers.Concatenate()([state_out, action_out])

    out = tf.keras.layers.Dense(256, activation="relu")(concat)
    out = tf.keras.layers.Dense(256, activation="relu")(out)
    outputs = tf.keras.layers.Dense(1, activation='linear')(out)

    # Outputs single value for give state-action
    model = tf.keras.Model([state_input, action_input], outputs, name="critic")

    return model


def create_actor(env: gym.Env):
    if env.action_space.__class__.__name__ == 'Box':
        action_dim = env.action_space.sample().shape[0]
    else:
        raise NotImplementedError(f'Action space of {env.action_space.__class__.__name__} not implemented')

    state_dim = env.observation_space.sample().shape

    inputs = tf.keras.layers.Input(shape=(state_dim))
    dense = tf.keras.layers.Dense(64, activation='relu')(inputs)
    dense = tf.keras.layers.Dense(64, activation='relu')(dense)
    output = tf.keras.layers.Dense(action_dim, activation='sigmoid')(dense)

    model = tf.keras.Model(inputs=inputs, outputs=output, name="actor")

    return model


def train(epoch, actor_optimizer, critic_optimizer, actor, target_actor, critic, target_critic, samples,
          gamma: float, tau: float):
    target_actions = target_actor(samples['next_states'], training=False)
    y = samples['rewards'] + tf.expand_dims(1 - samples['dones'], axis=1) * gamma * target_critic(
        [samples['next_states'], target_actions], training=False
    )

    with tf.GradientTape() as critic_tape:
        critic_value = critic([samples['states'], samples['actions']], training=True)
        critic_loss = tf.math.reduce_mean(tf.math.square(y - critic_value))

    critic_grad = critic_tape.gradient(critic_loss, critic.trainable_variables)
    critic_optimizer.apply_gradients(
        zip(critic_grad, critic.trainable_variables)
    )

    tf.summary.scalar('ddpg/state_val', data=tf.reduce_mean(critic_value), step=epoch)

    with tf.GradientTape() as actor_tape:
        actions = actor(samples['states'], training=True)
        critic_value = critic([samples['states'], actions], training=False)
        actor_loss = -tf.math.reduce_mean(critic_value)

    actor_grad = actor_tape.gradient(actor_loss, actor.trainable_variables)
    actor_optimizer.apply_gradients(
        zip(actor_grad, actor.trainable_variables)
    )

    update_target(target_actor.weights, actor.weights, tau=tau)
    update_target(target_critic.weights, critic.weights, tau=tau)

    tf.summary.scalar('ddpg/critic_loss', data=critic_loss, step=epoch)
    tf.summary.scalar('ddpg/actor_loss', data=actor_loss, step=epoch)


def update_target(target_weights, weights, tau):
    for (a, b) in zip(target_weights, weights):
        a.assign(a * (1 - tau) + b * tau)


def main(logdir):
    print(f'Starting thraining with {custom_ddpg_config["cpu_count"]} cpus. Logging to {logdir}')

    with ThreadPool(custom_ddpg_config["cpu_count"]) as pool:
        envs = pool.starmap(RemoteEnv,
                            [('localhost', 6985, env_config) for _ in range(custom_ddpg_config["cpu_count"])])

    critic = create_critic(envs[0])
    target_critic = create_critic(envs[0])
    for (a, b) in zip(target_critic.weights, critic.weights):
        a.assign(b)

    actor = create_actor(envs[0])
    target_actor = create_actor(envs[0])
    for (a, b) in zip(target_actor.weights, actor.weights):
        a.assign(b)

    critic.summary()
    actor.summary()

    actor_optimizer = tf.keras.optimizers.Adam(learning_rate=custom_ddpg_config["actor_lr"])
    critic_optimizer = tf.keras.optimizers.Adam(learning_rate=custom_ddpg_config["critic_lr"])

    buffer = ExperienceReplayBuffer(buffer_size=custom_ddpg_config["buffer_size"],
                                    batch_size=custom_ddpg_config["batch_size"])

    with ThreadPool(processes=custom_ddpg_config["cpu_count"]) as tp:
        try:
            for epoch in tqdm(range(custom_ddpg_config["training_epochs"])):
                trajectories = tp.starmap(get_single_trajectory, [(env, actor) for env in envs])
                for t in trajectories:
                    buffer.add(t)

                tf.summary.scalar('env/return',
                                  data=tf.reduce_mean([tf.reduce_sum(t['rewards']) for t in trajectories]), step=epoch)
                tf.summary.scalar('env/length', data=tf.reduce_mean([float(len(t['states'])) for t in trajectories]),
                                  step=epoch)

                tf.summary.scalar('power_grid/gamma+alpha/min', data=tf.reduce_min(
                    [tf.reduce_min([a[0] for a in t['scaled_actions']]) for t in trajectories]), step=epoch)
                tf.summary.scalar('power_grid/gamma+alpha/max', data=tf.reduce_max(
                    [tf.reduce_max([a[0] for a in t['scaled_actions']]) for t in trajectories]), step=epoch)
                tf.summary.scalar('power_grid/gamma+alpha/mean', data=tf.reduce_mean(
                    [tf.reduce_mean([a[0] for a in t['scaled_actions']]) for t in trajectories]), step=epoch)

                # tf.summary.scalar('power_grid/beta', data=tf.reduce_min(
                #     [tf.reduce_min([a[1] for a in t['scaled_actions']]) for t in trajectories]), step=epoch)
                # tf.summary.scalar('power_grid/beta', data=tf.reduce_max(
                #     [tf.reduce_max([a[1] for a in t['scaled_actions']]) for t in trajectories]), step=epoch)
                # tf.summary.scalar('power_grid/beta', data=tf.reduce_mean(
                #     [tf.reduce_mean([a[1] for a in t['scaled_actions']]) for t in trajectories]), step=epoch)

                # tf.summary.scalar('power_grid/gamma', data=tf.reduce_min(
                #     [tf.reduce_min([a[2] for a in t['scaled_actions']]) for t in trajectories]), step=epoch)
                # tf.summary.scalar('power_grid/gamma', data=tf.reduce_max(
                #     [tf.reduce_max([a[2] for a in t['scaled_actions']]) for t in trajectories]), step=epoch)
                # tf.summary.scalar('power_grid/gamma', data=tf.reduce_mean(
                #     [tf.reduce_mean([a[2] for a in t['scaled_actions']]) for t in trajectories]), step=epoch)

                # tf.summary.scalar('power_grid/c', data=tf.reduce_min(
                #     [tf.reduce_min([a[3] for a in t['scaled_actions']]) for t in trajectories]), step=epoch)
                # tf.summary.scalar('power_grid/c', data=tf.reduce_max(
                #     [tf.reduce_max([a[3] for a in t['scaled_actions']]) for t in trajectories]), step=epoch)
                # tf.summary.scalar('power_grid/c', data=tf.reduce_mean(
                #     [tf.reduce_mean([a[3] for a in t['scaled_actions']]) for t in trajectories]), step=epoch)

                tf.summary.scalar('trajectories/min_volt', data=tf.reduce_min(
                    [tf.reduce_min([tf.split(a, 2)[0] for a in t['states']]) for t in trajectories]), step=epoch)
                tf.summary.scalar('trajectories/max_volt', data=tf.reduce_max(
                    [tf.reduce_max([tf.split(a, 2)[0] for a in t['states']]) for t in trajectories]), step=epoch)

                tf.summary.scalar('trajectories/min_reactive', data=tf.reduce_min(
                    [tf.reduce_min([tf.split(a, 2)[1] for a in t['states']]) for t in trajectories]), step=epoch)
                tf.summary.scalar('trajectories/max_reactive', data=tf.reduce_max(
                    [tf.reduce_max([tf.split(a, 2)[1] for a in t['states']]) for t in trajectories]), step=epoch)

                if len(buffer.buffer) > buffer.batch_size:
                    for _ in range(max(1, int(sum([len(t['states']) for t in trajectories]) / buffer.batch_size * 8))):
                        train(epoch,
                              actor_optimizer, critic_optimizer,
                              actor, target_actor, critic, target_critic,
                              buffer.sample(),
                              gamma=env_config['gamma'],
                              tau=custom_ddpg_config["tau"])
        except KeyboardInterrupt:
            pass

    print('Saving actor and critic weights...')
    actor.save(logdir + '/actor.h5')
    critic.save(logdir + '/critic.h5')
    print(f'Actor and Critic Saved to {logdir}')


def evaluate(env, trial_name):
    actor = create_actor(env)
    critic = create_critic(env)

    actor.load_weights(f'logs/ddpg/{trial_name}/actor.h5')
    critic.load_weights(f'logs/ddpg/{trial_name}/critic.h5')

    return get_single_trajectory(env, actor)


if __name__ == '__main__':

    try:
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)

        logdir = "logs/ddpg/" + datetime.now().strftime("%Y%m%d-%H%M%S")
        file_writer = tf.summary.create_file_writer(logdir + "/metrics")
        file_writer.set_as_default()

        main(logdir)
    except RuntimeError as e:
        print(f'Failed to set GPU growth: {e}')

# if __name__ == '__main__':
#     trajectory = evaluate(env=RemoteEnv('localhost', 6985, env_config),
#              trial_name='20220727-171740')
#     print(trajectory)
