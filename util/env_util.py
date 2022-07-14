import gym
import numpy as np
import tensorflow as tf


class Historitized(gym.Env):

    def __init__(self, env: gym.Env, history_size) -> None:

        self.history = []
        self.history_size = history_size
        self.env = env

        self.action_space = self.env.action_space
        self.observation_space = gym.spaces.Box(low=np.tile(self.env.observation_space.low, self.history_size),
                                                high=np.tile(self.env.observation_space.high, self.history_size))

    def step(self, action):
        obs, reward, done, info = self.env.step(action)
        self.history.append(obs)
        if len(self.history) > self.history_size:
            del self.history[0]
        return np.array(self.history).flatten(), reward, done, info

    def reset(self):
        initial_obs = self.env.reset()
        self.history = [initial_obs] * self.history_size
        return np.array(self.history).flatten()

    def close(self):
        self.env.close()

    def render(self, mode='human'):
        return self.env.render(mode)


def get_rewards(env_config, states, rewards, dones):
    voltages, reactive_powers = tf.split(states, 2, axis=1)
    ret = tf.TensorArray(voltages.dtype, size=states.shape[0])
    ret = ret.write(0, rewards[0])

    for t in range(1, len(states)):
        if rewards[t] <= -1:
            ret = ret.write(t, -1)
        elif tf.reduce_all(tf.abs(voltages[t] - 1) < env_config['voltage_threshold'] * 1.023) and \
                tf.reduce_all(tf.abs(reactive_powers[t:t+env_config['window_size'], :] - reactive_powers[t, :]) < env_config['change_threshold']):
            ret = ret.write(t, 1)
            dones[t] = True
        else:
            voltage_deviation = tf.reduce_mean(tf.abs(voltages[t] - 1) - env_config['voltage_threshold'])
            reactive_power_deviation = tf.reduce_mean(tf.clip_by_value(tf.abs(reactive_powers[t:t+env_config['window_size'], :] - reactive_powers[t, :]) - env_config['change_threshold'], 0.0, voltages.dtype.max))
            reward = (tf.exp(-voltage_deviation) + tf.exp(-reactive_power_deviation) - 2) * env_config['gamma']
            ret = ret.write(t, reward)

    return ret.stack()
