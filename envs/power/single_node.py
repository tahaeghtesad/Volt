import gym
import numpy as np

from envs.power.thirteen_bus import ThirteenBus


class SingleNode(gym.Env):
    def __init__(self, index, config):
        self.env = ThirteenBus(config)
        self.index = index
        self.action_space = gym.spaces.Box(0, 10_000, (4,))
        self.observation_space = gym.spaces.Box(-10_000, 10_000, (2,))

        self.alpha = 0.001
        self.beta = 5
        self.gamma = 200
        self.c = 1

        self.n = 1
        self.T = self.env.T

    def reset(self):
        full_obs = self.env.reset()
        return np.array([full_obs[self.index], full_obs[-1]])

    def step(self, action: np.ndarray):
        full_action = np.concatenate((
            self.alpha * np.ones(self.env.n),
            self.beta * np.ones(self.env.n),
            self.gamma * np.ones(self.env.n),
            self.c * np.ones(self.env.n),
        ))

        full_action[self.env.n * 0 + self.index] = action[0]
        full_action[self.env.n * 1 + self.index] = action[1]
        full_action[self.env.n * 2 + self.index] = action[2]
        full_action[self.env.n * 3 + self.index] = action[3]

        full_obs, reward, done, info = self.env.step(full_action)

        return np.array([full_obs[self.index], full_obs[-1]]), - info['q'][self.index][0] - info['fes'], done, info

    def render(self, mode='human'):
        raise NotImplementedError()
