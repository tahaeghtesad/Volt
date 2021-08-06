import gym
import numpy as np

from envs.power.thirteen_bus import ThirteenBus


class SingleParamThirteenBus(gym.Env):
    def __init__(self, engine_pool, config):
        self.env = ThirteenBus(engine_pool, config)

        self.action_space = gym.spaces.Box(-config['search_range'], config['search_range'], (4,))

        self.observation_space = self.env.observation_space

        self.n = self.env.n
        self.T = self.env.T

    def reset(self):
        return self.env.reset()

    def step(self, action: np.ndarray):
        action = np.power(10, action)
        full_action = np.concatenate((
            np.ones(self.env.n) * action[0],
            np.ones(self.env.n) * action[1],
            np.ones(self.env.n) * action[2],
            np.ones(self.env.n) * action[3],
        ))

        return self.env.step(full_action)

    def close(self):
        self.env.close()

    def render(self, mode='human'):
        self.env.render(mode)
