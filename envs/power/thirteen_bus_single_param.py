import gym
import numpy as np

from envs.power.thirteen_bus import ThirteenBus


class SingleParamThirteenBus(gym.Env):
    def __init__(self, engine_pool, config):
        self.env = ThirteenBus(engine_pool, config)

        self.action_space = gym.spaces.Box(low=-self.env.env_config['search_range'],
                                           high=self.env.env_config['search_range'],
                                           shape=(4,))

        # self.action_space = gym.spaces.Box(low=np.log10(np.array([1e-3, 1e-1, 1e-1, 1e-2])),
        #                                    high=np.log10(np.array([1e1, 1e2, 1e2, 1e2])))

        self.observation_space = self.env.observation_space

        self.n = self.env.n
        self.T = self.env.T

    def reset(self):
        return self.env.reset()

    def step(self, action: np.ndarray):
        full_action = action.repeat(self.n)

        return self.env.step(full_action)

    def close(self):
        self.env.close()

    def render(self, mode='human'):
        self.env.render(mode)
