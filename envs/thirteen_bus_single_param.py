import gym
import numpy as np

from envs.power.thirteen_bus import ThirteenBus


class SingleParamThirteenBus(gym.Env):
    def __init__(self, config):
        self.env = ThirteenBus(config)
        self.index = config['index']
        self.search_range = config['search_range']

        self.action_space = gym.spaces.Box(-self.search_range, self.search_range, (4,))

        self.observation_space = self.env.observation_space

        self.alpha = config['alpha']
        self.beta = config['beta']
        self.gamma = config['gamma']
        self.c = config['c']

        self.n = self.env.n
        self.T = self.env.T

    def reset(self):
        return self.env.reset()

    def step(self, action: np.ndarray):
        full_action = np.concatenate((
            self.alpha * (np.ones(self.env.n) + action[0]),
            self.beta * (np.ones(self.env.n) + action[1]),
            self.gamma * (np.ones(self.env.n) + action[2]),
            self.c * (np.ones(self.env.n) + action[3]),
        ))

        return self.env.step(full_action)

    def close(self):
        self.env.close()

    def render(self, mode='human'):
        self.env.render(mode)
