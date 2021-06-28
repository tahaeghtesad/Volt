import datetime
import io
import sys

import gym
import time
import matlab.engine
import numpy as np


class ThirteenBus(gym.Env):
    def __init__(self, env_config):
        # if engine is None:
        self.env_config = env_config
        start = time.time()
        print('Starting matlab engine...')
        self.engine = matlab.engine.start_matlab()
        self.engine.addpath('C:\\Users\\Taha\\PycharmProjects\\Volt\\envs\\power\\matlab')

        print(f'Matlab engine started in {time.time() - start:.2f} seconds.')
        # else:
        #     self.engine = engine

        self.null_stream = io.StringIO()

        self.T = self.engine.workspace['T'] = 1000
        # self.engine.Power_system_initialization(nargout=0, stdout=self.null_stream)

        # self.n = int(self.engine.workspace['n'])
        self.n = 29

        self.step_number = 0
        self.episode = 0

        self.action_space = gym.spaces.Box(0, 10000, (4 * self.n,))
        self.observation_space = gym.spaces.Box(-10000, 10000, (self.n + 1,))

    def reset(self):
        self.episode += 1
        self.step_number = 0

        self.engine.eval('clc', nargout=0)
        self.engine.Power_system_initialization(nargout=0, stdout=self.null_stream)

        return np.concatenate((np.zeros((self.n, 1)).flatten(), np.zeros((1, ))))

    def step(self, action: np.ndarray):  # -> observation, reward, done, info
        self.step_number += 1
        var = self.engine.step(matlab.double(action[0 * self.n: 1 * self.n].reshape(self.n, 1).tolist()),
                               matlab.double(action[1 * self.n: 2 * self.n].reshape(self.n, 1).tolist()),
                               matlab.double(action[2 * self.n: 3 * self.n].reshape(self.n, 1).tolist()),
                               matlab.double(action[3 * self.n: 4 * self.n].reshape(self.n, 1).tolist()),
                               self.step_number, stdout=self.null_stream)

        v = np.array(var['v'], dtype=np.float)
        q = np.array(var['q'], dtype=np.float)
        fes = np.array([var['fes']], dtype=np.float)

        obs = np.concatenate((v.flatten(), fes))
        q_norm = np.linalg.norm(q)
        reward = -q_norm - fes[0]
        done = self.step_number == self.T

        # if done:
        #     print(f'Step: {self.step_number}')

        # print(f'Step: {self.step_number} - q_norm: {q_norm} - fes: {fes} - reward: {reward}')

        return obs, reward, done, {'v': v, 'q': q, 'fes': fes[0]}

    def render(self, mode='human'):
        raise NotImplementedError()

    def close(self):
        self.engine.quit()
        print('Matlab closed.')
