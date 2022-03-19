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
        self.engine.addpath(f'C:\\Users\\teghtesa\\PycharmProjects\\Volt\\envs\\power\\{env_config["system"]}_{env_config["mode"]}')

        self.null_stream = io.StringIO()

        self.T = self.env_config['T']

        self.engine.workspace['T'] = int(1.5 * self.T + 1)
        self.engine.Power_system_initialization(nargout=0, stdout=self.null_stream)

        self.n = int(self.engine.workspace['n'])

        self.step_number = 0
        self.episode = 0

        # self.action_space = gym.spaces.Box(np.log10(np.repeat(np.array([1e2, 1e-3, 1e-1, 1e-1]), self.n)),
        #                                    np.log10(np.repeat(np.array([1e-10, 1e3, 1e10, 1e4]), self.n)))

        self.action_space = gym.spaces.Box(low=-self.env_config['search_range'],
                                           high=self.env_config['search_range'],
                                           shape=(self.n * 4,))

        self.observation_space = gym.spaces.Box(-10000, 10000, (self.n * 2 + 1,))  # q, v, time

        self.q_history = [[] for _ in range(self.n)]
        self.prev_q = np.zeros(self.n)

    def reset(self):
        self.episode += 1
        self.step_number = 0

        self.engine.eval('clc', nargout=0)
        self.engine.workspace['T'] = int(1.5 * self.T + 1)
        # self.engine.workspace['load_var'] = float(np.random.random() * 0.4 + 0.8)
        self.engine.workspace['load_var'] = self.env_config['load_var']
        self.engine.Power_system_initialization(nargout=0, stdout=self.null_stream)

        self.q_history = [[] for _ in range(self.n)]

        self.prev_q = np.zeros(self.n)

        return np.zeros(self.n * 2 + 1)

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
            self.logger.error(f'Action Value: {action}')
            raise e

        info = dict(
            v=np.array(var['v'], dtype=np.float),
            q=np.array(var['q'], dtype=np.float),
            fes=np.array([var['fes']], dtype=np.float),
            f=np.array([var['f']], dtype=np.float),
        )

        obs = np.concatenate((info['v'].flatten(), self.prev_q - info['q'].flatten(), np.array([self.step_number])))
        self.prev_q = info['q'].flatten()

        for c in range(self.n):
            self.q_history[c].append(info['q'][c][0])
            if len(self.q_history[c]) > self.env_config['window_size']:
                del self.q_history[c][0]

        voltages_converged = np.all(np.abs(info['v'] - 1) < self.env_config['voltage_threshold'] * 1.1)
        voltage_deviations = np.mean(np.clip(np.abs(info['v'] - 1) - self.env_config['voltage_threshold'], 0, None))
        changes = np.mean([np.mean(np.clip(
            np.abs(self.q_history[c][-1] - np.array(self.q_history[c])) / self.q_history[c][-1] - self.env_config[
                'change_threshold'], 0, None)) for c in range(self.n)])

        changes_converged = \
            len(self.q_history[0]) >= self.env_config['window_size'] and \
            all([np.all(
                np.abs(self.q_history[c][-1] - np.array(self.q_history[c])) / self.q_history[c][-1] < self.env_config[
                    'change_threshold'] * 1.05) for c in range(self.n)])

        converged = voltages_converged and changes_converged

        info['changes'] = changes
        info['voltage_deviations'] = voltage_deviations

        done = self.step_number == self.T // self.env_config['repeat'] or converged or (
               self.env_config['reward_mode'] == 'continuous' and
               not voltages_converged and
               self.step_number * self.env_config['repeat'] >= self.env_config['voltage_convergence_grace_period'])

        reward = -1  # This is not required!

        if self.env_config['reward_mode'] == 'continuous':
            reward = 0

            reward += np.exp(-changes)
            reward += np.exp(-voltage_deviations)

            if converged:
                reward += 3 * (self.env_config['T'] // self.env_config['repeat'] - self.step_number + 1)  # This number is multiplied by 2 since max step reward for each step is 2!

            reward *= 0.01

        elif self.env_config['reward_mode'] == 'steps':
            if converged:
                reward = 0
            else:
                reward = -1


        # reward = -1 if not voltages_converged else 0

        # reward = 0 if converged else -1 - 0.5 * voltage_deviations - 0.01 * changes

        # if done:
        #     print(f'Step: {self.step_number}')

        # print(f'Step: {self.step_number} - q_norm: {q_norm} - fes: {fes} - reward: {reward}')

        return obs, reward, done, info

    def render(self, mode='human'):
        raise NotImplementedError()

    def close(self):
        if self.matlab_running is True:
            self.matlab_running = False
            self.engine_pool.release(self.engine)
            self.logger.info('Matlab closed.')
