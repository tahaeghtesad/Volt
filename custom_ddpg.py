import threading
from datetime import datetime
from multiprocessing.pool import ThreadPool

import gym
import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
from tqdm import tqdm

from envs.remote.client import RemoteEnv
from config import env_config
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
    noise = OUActionNoise(np.zeros(env.action_space.low.shape[0]), std_deviation=0.1 * np.ones(env.action_space.low.shape[0]))
    done = False

    while not done:
        action = actor(np.array([observation]))[0] + noise()
        scaled_action = tf.sigmoid(action) * (env.action_space.high - env.action_space.low) + env.action_space.low

        new_obs, reward, done, info = env.step(scaled_action)

        states.append(observation)
        actions.append(action)
        scaled_actions.append(scaled_action)
        rewards.append(reward)
        next_states.append(new_obs)
        dones.append(done)

        observation = new_obs

    rewards = get_rewards(env_config, np.array(states), np.array(rewards))
    convergence_time = np.where(rewards == 1)[0]
    if len(convergence_time) > 0:
        convergence_time = convergence_time[0] + 1
        print(f'Converged at step {convergence_time}')
    else:
        convergence_time = None

    return dict(
        states=np.array(states, dtype=np.float32)[:convergence_time],
        actions=np.array(actions, dtype=np.float32)[:convergence_time],
        scaled_actions=np.array(scaled_actions, dtype=np.float32)[:convergence_time],
        rewards=np.array(rewards[:convergence_time], dtype=np.float32),
        next_states=np.array(next_states, dtype=np.float32)[:convergence_time],
        dones=np.array(dones, dtype=np.float32)[:convergence_time],
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
            + self.std_dev * np.sqrt(self.dt) * np.random.normal(size=self.mean.shape)
        )
        # Store x into x_prev
        # Makes next noise dependent on current one
        self.x_prev = x
        return x

    def reset(self):
        if self.x_initial is not None:
            self.x_prev = self.x_initial
        else:
            self.x_prev = np.zeros_like(self.mean)


class ExperienceReplayBuffer:
    def __init__(self, buffer_size, sample_size):
        self.buffer_size = buffer_size
        self.sample_size = sample_size
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
        indices = np.random.choice(len(self.buffer), self.sample_size, replace=False)
        ret = dict(
            states=[],
            actions=[],
            scaled_actions=[],
            rewards=[],
            next_states=[],
            dones=[],
        )

        for i in indices:
            ret['states'].append(self.buffer[i]['state'])
            ret['actions'].append(self.buffer[i]['action'])
            ret['scaled_actions'].append(self.buffer[i]['scaled_action'])
            ret['rewards'].append(self.buffer[i]['reward'])
            ret['next_states'].append(self.buffer[i]['next_state'])
            ret['dones'].append(self.buffer[i]['done'])

        return {k: np.array(v) for k, v in ret.items()}


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
    outputs = tf.keras.layers.Dense(1)(out)

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
    output = tf.keras.layers.Dense(action_dim, activation='linear')(dense)

    model = tf.keras.Model(inputs=inputs, outputs=output, name="actor")

    return model


def train(epoch, optimizer, actor, target_actor, critic, target_critic, samples,
          gamma: float, tau: float):

    with tf.GradientTape() as actor_tape, tf.GradientTape() as critic_tape:
        target_actions = target_actor(samples['next_states'])
        y = samples['rewards'] + gamma * target_critic(
            [samples['next_states'], target_actions], training=True
        )
        critic_value = critic([samples['states'], samples['actions']], training=True)
        critic_loss = tf.math.reduce_mean(tf.math.square(y - critic_value))

        actions = actor(samples['states'], training=True)
        critic_value = critic([samples['states'], actions], training=True)
        # Used `-value` as we want to maximize the value given
        # by the critic for our actions
        actor_loss = -tf.math.reduce_mean(critic_value)

    critic_grad = critic_tape.gradient(critic_loss, critic.trainable_variables)
    optimizer.apply_gradients(
        zip(critic_grad, critic.trainable_variables)
    )

    actor_grad = actor_tape.gradient(actor_loss, actor.trainable_variables)
    optimizer.apply_gradients(
        zip(actor_grad, actor.trainable_variables)
    )

    update_target(target_actor.weights, actor.weights, tau=tau)
    update_target(target_critic.weights, critic.weights, tau=tau)

    tf.summary.scalar('ddpg/state_val', data=tf.reduce_mean(critic_value), step=epoch)
    tf.summary.scalar('ddpg/critic_loss', data=critic_loss, step=epoch)
    tf.summary.scalar('ppo/actor_loss', data=actor_loss, step=epoch)


def update_target(target_weights, weights, tau):
    for (a, b) in zip(target_weights, weights):
        a.assign(b * tau + a * (1 - tau))


def main(numcpus):

    with ThreadPool(numcpus) as pool:
        envs = pool.starmap(RemoteEnv, [('localhost', 6985, env_config) for _ in range(numcpus)])

    critic = create_critic(envs[0])
    target_critic = create_critic(envs[0])
    actor = create_actor(envs[0])
    target_actor = create_actor(envs[0])

    critic.summary()
    actor.summary()

    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)  # this should depend on the number of training epochs.
    buffer = ExperienceReplayBuffer(buffer_size=10000, sample_size=64)

    with ThreadPool(processes=numcpus) as tp:

        for epoch in tqdm(range(1000)):
            trajectories = tp.starmap(get_single_trajectory, [(env, target_actor) for env in envs])
            for t in trajectories:
                buffer.add(t)

            if len(buffer.buffer) > buffer.sample_size:
                train(epoch, optimizer, actor, target_actor, critic, target_critic, buffer.sample(), gamma=0.99, tau=0.001)


if __name__ == '__main__':

    logdir = "logs/tb_logs/ddpg/" + datetime.now().strftime("%Y%m%d-%H%M%S")
    file_writer = tf.summary.create_file_writer(logdir + "/metrics")
    file_writer.set_as_default()

    main(8)