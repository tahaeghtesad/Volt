import datetime
import io
import sys

import gym
import time
import matlab.engine
import numpy as np

import logging

from util.reusable_pool import ReusablePool


class ThirteenBus(gym.Env):
    def __init__(self, engine_pool: ReusablePool, env_config):
        self.logger = logging.getLogger(__name__)
        self.matlab_running = False
        self.engine_pool = engine_pool

        self.env_config = env_config

        self.engine = self.engine_pool.acquire()

        self.null_stream = io.StringIO()

        self.T = self.env_config['T']
        # self.engine.Power_system_initialization(nargout=0, stdout=self.null_stream)

        # self.n = int(self.engine.workspace['n'])
        self.n = 29

        self.step_number = 0
        self.episode = 0

        self.action_space = gym.spaces.Box(-self.env_config['search_range'], self.env_config['search_range'], (4 * self.n,))
        self.observation_space = gym.spaces.Box(-10000, 10000, (self.n,))

        self.reward_history = []

    def reset(self):
        self.episode += 1
        self.step_number = 0

        init_vol = (1 - 0.9025) * np.random.rand(self.n, 1) + 0.9025

        self.engine.workspace['T'] = self.T
        self.engine.workspace['init_vol'] = matlab.double(init_vol.tolist())

        self.engine.Power_system_initialization(nargout=0, stdout=self.null_stream)

        # obs, reward, done, info = self.step(np.repeat(np.array([self.env_config['defaults']['alpha'],
        #                                               self.env_config['defaults']['beta'],
        #                                               self.env_config['defaults']['gamma'],
        #                                               self.env_config['defaults']['c']]), self.n))

        self.reward_history = []

        return init_vol.flatten()

    def step(self, action: np.ndarray):  # -> observation, reward, done, info
        # action = np.power(10, action)
        self.step_number += 1
        var = self.engine.step(matlab.double(action[0 * self.n: 1 * self.n].reshape(self.n, 1).tolist()),
                               matlab.double(action[1 * self.n: 2 * self.n].reshape(self.n, 1).tolist()),
                               matlab.double(action[2 * self.n: 3 * self.n].reshape(self.n, 1).tolist()),
                               matlab.double(action[3 * self.n: 4 * self.n].reshape(self.n, 1).tolist()),
                               self.step_number, stdout=self.null_stream)

        v = np.array(var['v'], dtype=np.float)
        q = np.array(var['q'], dtype=np.float)
        fes = np.array([var['fes']], dtype=np.float)
        f = np.array([var['f']], dtype=np.float)

        obs = v.flatten()
        # q_norm = np.linalg.norm(q)
        # reward = -q_norm - fes[0]
        reward = - f[0]
        self.reward_history.append(reward)
        if len(self.reward_history) > 32:
            del self.reward_history[0]

        done = self.step_number == self.T

        # if done:
        #     print(f'Step: {self.step_number}')

        # print(f'Step: {self.step_number} - q_norm: {q_norm} - fes: {fes} - reward: {reward}')

        return obs, reward, done, {'v': v, 'q': q, 'fes': fes[0], 'f': f[0]}

    def render(self, mode='human'):
        raise NotImplementedError()

    def close(self):
        if self.matlab_running is True:
            self.matlab_running = False
            self.engine_pool.release(self.engine)
            self.logger.info('Matlab closed.')
