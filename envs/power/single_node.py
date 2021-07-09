import gym
import numpy as np

from envs.power.thirteen_bus import ThirteenBus


class SingleNode(gym.Env):
    def __init__(self, index, config):
        self.env = ThirteenBus(config)
        self.index = index
        self.action_space = gym.spaces.Box(0, 10_000, (4,))
        self.observation_space = gym.spaces.Box(-10_000, 10_000, (3,))

        self.alpha = 0.001
        self.beta = 5
        self.gamma = 200
        self.c = 1

        self.n = 1
        self.T = self.env.T

    def reset(self):
        self.env.reset()
        return np.array([0., 0., 0.])

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

        return np.array([full_obs[self.env.n * 0 + self.index],
                         full_obs[self.env.n * 1 + self.index],
                         full_obs[-1]]
                        ), reward, done, info

    def __del__(self):
        self.close()

    def close(self):
        self.env.close()

    def render(self, mode='human'):
        raise NotImplementedError()
