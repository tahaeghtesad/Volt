import gym
import numpy as np

from envs.power.thirteen_bus import ThirteenBus


class SingleParamThirteenBus(gym.Env):
    def __init__(self, engine_pool, config):
        self.env = ThirteenBus(engine_pool, config)

        self.action_space = gym.spaces.Box(np.log10(np.array([1e-5, 0.1,  100.0, 0.1])),
                                           np.log10(np.array([1.0, 10.0, 300.0, 10.0])))

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
