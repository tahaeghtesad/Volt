import datetime
import io
import sys

import gym
import time
import matlab.engine
import numpy as np


class ThirteenBus(gym.Env):
    def __init__(self, env_config=None):
        # if engine is None:
        start = time.time()
        print('Starting matlab engine...')
        self.engine = matlab.engine.start_matlab()
        self.engine.addpath('C:\\Users\\Taha\\PycharmProjects\\Volt\\envs\\power\\matlab')

        print(f'Matlab engine started in {time.time() - start:.2f} seconds.')
        # else:
        #     self.engine = engine

        self.null_stream = io.StringIO()

        self.engine.Power_system_initialization(nargout=0, stdout=self.null_stream)

        self.T = int(self.engine.workspace['T'])
        self.n = int(self.engine.workspace['n'])

        self.step_number = 0
        self.episode = 0

        self.action_space = gym.spaces.Box(0, 10000, (4 * self.n,))
        self.observation_space = gym.spaces.Box(-10000, 1000, (self.n * self.T * 2 + self.T,))
        self.env_config = env_config

    def reset(self):
        self.episode += 1
        self.step_number = 0

        self.engine.Power_system_initialization(nargout=0, stdout=self.null_stream)
        var = self.engine.workspace['var']

        v = np.array(var['v'], dtype=np.float32)
        q = np.array(var['q'], dtype=np.float32)
        fes = np.array(var['fes'], dtype=np.float32)

        return np.concatenate((v.flatten(), q.flatten(), fes.flatten()))

    def step(self, action: np.ndarray):  # -> observation, reward, done, info
        self.step_number += 1
        start = datetime.datetime.now()
        var = self.engine.step(matlab.double(action[0 * self.n: 1 * self.n].reshape(self.n, 1).tolist()),
                               matlab.double(action[1 * self.n: 2 * self.n].reshape(self.n, 1).tolist()),
                               matlab.double(action[2 * self.n: 3 * self.n].reshape(self.n, 1).tolist()),
                               matlab.double(action[3 * self.n: 4 * self.n].reshape(self.n, 1).tolist()),
                               self.step_number, stdout=self.null_stream)

        v = np.array(var['v'], dtype=np.float32)
        q = np.array(var['q'], dtype=np.float32)
        fes = np.array(var['fes'], dtype=np.float32)

        return np.concatenate((v.flatten(), q.flatten(), fes.flatten())), \
               np.linalg.norm(-v[:, self.step_number] ** 2) - fes[0][self.step_number],\
               self.step == self.T,\
               {
                   'v': v,
                   'q': q,
                   'fes': fes
               }

    def render(self, mode='human'):
        raise NotImplementedError()
