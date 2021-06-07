import gym
import time
import matlab.engine
import numpy as np


class ThirteenBus(gym.Env):
    def __init__(self, engine=None):
        if engine is None:
            start = time.time()
            print('Starting matlab engine...')
            self.engine = matlab.engine.start_matlab()
            self.engine.addpath(self.engine.genpath('./matlab'))

            print(f'Matlab engine started in {time.time() - start:.2f} seconds.')
        else:
            self.engine = engine

        self.engine.Power_system_initialization(nargout=0)

        self.T = int(self.engine.workspace['T'])
        self.n = int(self.engine.workspace['n'])

        self.step_number = 0
        self.episode = 0

        self.action_space = gym.spaces.Box(0, 10000, (4, self.n))
        self.observation_space = gym.spaces.Box(-10000, 1000, (self.n * self.T * 2 + self.n,))

    def reset(self):

        self.episode += 1
        self.step_number = 0

        self.engine.Power_system_initialization(nargout=0)
        var = self.engine.create_var()

        return np.array([var['v'], var['q'], var['fes']]).flatten()

    def step(self, action: np.ndarray):  # -> observation, reward, done, info

        self.step_number += 1

        var = self.engine.optdist_vc_ML(action[0, :].reshape(self.n, 1).tolist(), action[1, :].reshape(self.n, 1).tolist(), action[2, :].reshape(self.n, 1).tolist(), action[3, :].reshape(self.n, 1).tolist(), self.step_number)

        return np.array([var['v'], var['q'], var['fes']]).flatten(), \
               np.linalg.norm(-np.array(var['v']) ** 2 - np.array(var['fes'])),\
               self.step == self.T,\
               var

    def render(self, mode='human'):
        raise NotImplementedError()
