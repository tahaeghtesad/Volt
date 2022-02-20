import datetime
import io
import math
import sys

import gym
import time
import matlab.engine
import numpy as np

import logging
from scipy.stats import linregress

from util.reusable_pool import ReusablePool


class ThirteenBus(gym.Env):
    def __init__(self, engine_pool: ReusablePool, env_config):
        self.logger = logging.getLogger(__name__)
        self.matlab_running = True
        self.engine_pool = engine_pool

        self.env_config = env_config

        self.engine = self.engine_pool.acquire()
        self.engine.addpath('C:\\Users\\teghtesa\\PycharmProjects\\Volt\\envs\\power\\ieee13_all_control')

        self.null_stream = io.StringIO()

        self.T = self.env_config['T']
        # self.engine.Power_system_initialization(nargout=0, stdout=self.null_stream)

        # self.n = int(self.engine.workspace['n'])
        self.n = 29

        self.step_number = 0
        self.episode = 0

        self.action_space = gym.spaces.Box(np.log10(np.repeat(np.array([1e2, 1e-3, 1e-1, 1e-1]), self.n)),
                                           np.log10(np.repeat(np.array([1e-10, 1e3, 1e10, 1e4]), self.n)))
        self.observation_space = gym.spaces.Box(-10000, 10000, (self.n,))

        self.q_history = [[] for _ in range(self.n)]
        self.converged_history = []

    def reset(self):
        self.episode += 1
        self.step_number = 0

        self.engine.workspace['T'] = int(1.5 * self.T + 1)

        self.engine.eval('clc', nargout=0)
        self.engine.Power_system_initialization(nargout=0, stdout=self.null_stream)

        # obs, reward, done, info = self.step(np.repeat(np.array([self.env_config['defaults']['alpha'],
        #                                               self.env_config['defaults']['beta'],
        #                                               self.env_config['defaults']['gamma'],
        #                                               self.env_config['defaults']['c']]), self.n))

        self.q_history = [[] for _ in range(self.n)]
        self.converged_history = []

        return np.zeros((self.n, 1))

    def step(self, action: np.ndarray):  # -> observation, reward, done, info
        action = np.power(10, action)
        self.step_number += 1
        try:
            var = self.engine.step(matlab.double(action[0 * self.n: 1 * self.n].reshape(self.n, 1).tolist()),
                                   matlab.double(action[1 * self.n: 2 * self.n].reshape(self.n, 1).tolist()),
                                   matlab.double(action[2 * self.n: 3 * self.n].reshape(self.n, 1).tolist()),
                                   matlab.double(action[3 * self.n: 4 * self.n].reshape(self.n, 1).tolist()),
                                   self.env_config['repeat'],
                                   self.step_number, stdout=self.null_stream)
        except Exception as e:
            self.logger.error(f'Step: {self.step_number}')
            raise e

        v = np.array(var['v'], dtype=np.float)
        q = np.array(var['q'], dtype=np.float)
        fes = np.array([var['fes']], dtype=np.float)
        f = np.array([var['f']], dtype=np.float)

        obs = v.flatten()
        # q_norm = np.linalg.norm(q)
        # reward = -q_norm - fes[0]

        for c in range(self.n):
            self.q_history[c].append(q[c][0])
            if len(self.q_history[c]) > self.env_config['window_size']:
                del self.q_history[c][0]

        voltages_converged = all(np.abs(v - 1) < self.env_config['voltage_threshold'] * 1.05)
        max_q_slope = np.max([np.abs(linregress(np.arange(len(self.q_history[c])), self.q_history[c])[0]) for c in range(self.n)]) if len(self.q_history[0]) > 1 else np.nan

        q_slopes_converged = len(self.q_history[0]) > 1 and max_q_slope < 5e-5
        converged = voltages_converged and q_slopes_converged
        # print(str(self.step_number) + '\t' + str(converged) + '\t' + str(np.max([np.abs(linregress(np.arange(len(self.q_history[c])), self.q_history[c])[0]) for c in range(self.n)])))

        self.converged_history.append(converged)
        if len(self.converged_history) > 10:
            del self.converged_history[0]

        done = self.step_number == self.T // self.env_config['repeat'] or (all(self.converged_history) and len(self.converged_history) == 10)
        reward = 0 if converged else -1

        # if done:
        #     print(f'Step: {self.step_number}')

        # print(f'Step: {self.step_number} - q_norm: {q_norm} - fes: {fes} - reward: {reward}')

        return obs, reward, done, {'v': v, 'q': q, 'fes': fes[0], 'f': f[0], 'max_q_slope': max_q_slope}

    def render(self, mode='human'):
        raise NotImplementedError()

    def close(self):
        if self.matlab_running is True:
            self.matlab_running = False
            self.engine_pool.release(self.engine)
            self.logger.info('Matlab closed.')
