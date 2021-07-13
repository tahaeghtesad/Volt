import gym
import numpy as np


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
