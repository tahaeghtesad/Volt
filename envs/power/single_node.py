import gym
import numpy as np

from envs.power.matlab_wrapper import MatlabWrapperEnv


class SingleNode(gym.Env):
    def __init__(self, config):
        self.env = MatlabWrapperEnv(config)
        self.index = config['index']
        self.search_range = config['search_range']
        # self.action_space = gym.spaces.Box(
        #     low=np.array([
        #         self.env.action_space.low[self.env.n * 0 + self.index],
        #         self.env.action_space.low[self.env.n * 1 + self.index],
        #         self.env.action_space.low[self.env.n * 2 + self.index],
        #         self.env.action_space.low[self.env.n * 3 + self.index],
        # ]),
        #     high=np.array([
        #         self.env.action_space.high[self.env.n * 0 + self.index],
        #         self.env.action_space.high[self.env.n * 1 + self.index],
        #         self.env.action_space.high[self.env.n * 2 + self.index],
        #         self.env.action_space.high[self.env.n * 3 + self.index],
        #     ]))

        self.action_space = gym.spaces.Box(-self.search_range, self.search_range, (4,))

        self.observation_space = gym.spaces.Box(
            low=np.array([
                self.env.observation_space.low[self.env.n * 0 + self.index],
                self.env.observation_space.low[self.env.n * 1 + self.index],
            ]),
            high=np.array([
                self.env.observation_space.high[self.env.n * 0 + self.index],
                self.env.observation_space.high[self.env.n * 1 + self.index],
            ])
        )

        self.alpha = config['alpha']
        self.beta = config['beta']
        self.gamma = config['gamma']
        self.c = config['c']

        self.n = 1
        self.T = self.env.T

    def reset(self):
        full_obs = self.env.reset()
        return np.array([full_obs[self.env.n * 0 + self.index],
                         full_obs[self.env.n * 1 + self.index]])

    def step(self, action: np.ndarray):
        full_action = np.concatenate((
            self.alpha * np.ones(self.env.n),
            self.beta * np.ones(self.env.n),
            self.gamma * np.ones(self.env.n),
            self.c * np.ones(self.env.n),
        ))

        full_action[self.env.n * 0 + self.index] = self.alpha * (1 + action[0])
        full_action[self.env.n * 1 + self.index] = self.beta * (1 + action[1])
        full_action[self.env.n * 2 + self.index] = self.gamma * (1 + action[2])
        full_action[self.env.n * 3 + self.index] = self.c * (1 + action[3])

        full_obs, reward, done, info = self.env.step(full_action)

        return np.array([full_obs[self.env.n * 0 + self.index],
                         full_obs[self.env.n * 1 + self.index]]
                        ), np.max(0, np.abs(info['v'][self.index] - 1) - 0.05) ** 2, done, info

    def close(self):
        self.env.close()

    def render(self, mode='human'):
        raise NotImplementedError()
