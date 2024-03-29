import io
import logging
import random
import sys

import gym
import matlab.engine
import numpy as np
import shutil
import tempfile

from util.reusable_pool import ReusablePool


class MatlabWrapperEnv(gym.Env):
    def __init__(self, env_id, engine_pool: ReusablePool, env_config):

        # self.progress_bar = tqdm(total=env_config['T'] // env_config['repeat'], desc=f'{env_id}', position=env_id, leave=True)

        self.logger = logging.getLogger(__name__)
        self.env_id = env_id

        self.matlab_running = True
        self.engine_pool = engine_pool

        self.env_config = env_config

        # self.progress_bar.set_description(f'{env_id}|Starting Matlab...')

        self.temp_dir = tempfile.gettempdir() + f'\\tmp{random.randint(10000000, 99999999)}'
        shutil.copytree(
            f'C:\\Users\\teghtesa\\PycharmProjects\\Volt\\envs\\power\\{env_config["system"]}_{env_config["mode"]}',
            self.temp_dir)
        self.logger.debug(f'Copied {env_config["system"]}_{env_config["mode"]} to {self.temp_dir}')

        self.engine = self.engine_pool.acquire()
        self.engine.addpath(self.temp_dir)

        self.null_stream = io.StringIO()

        self.T = self.env_config['T']

        # self.progress_bar.set_description(f'{env_id}|Setting Config...')

        self.engine.workspace['T'] = int(1.5 * self.T + 1)
        self.engine.workspace['load_var'] = 1
        self.engine.workspace['TEMPDIR'] = self.temp_dir
        self.engine.Power_system_initialization(nargout=0, stdout=self.null_stream)

        self.n = int(self.engine.workspace['n'])

        self.step_number = 0
        self.episode = 0

        # self.action_space = gym.spaces.Box(np.log10(np.repeat(np.array([1e2, 1e-3, 1e-1, 1e-1]), self.n)),
        #                                    np.log10(np.repeat(np.array([1e-10, 1e3, 1e10, 1e4]), self.n)))

        self.action_space = gym.spaces.Box(low=np.repeat(np.array(self.env_config['range']['low']), self.n),
                                           high=np.repeat(np.array(self.env_config['range']['high']), self.n),
                                           shape=(self.n * 4,))

        self.observation_space = gym.spaces.Box(-10000, 10000, (self.n * 2,))  # q, v, time

        self.q_history = [[] for _ in range(self.n)]

    def reset(self):
        # self.progress_bar.reset()
        self.episode += 1
        self.step_number = 0

        # self.progress_bar.set_description(f'{self.env_id}|Resetting Environment...')

        self.engine.eval('clc', nargout=0)
        self.engine.workspace['T'] = int(1.5 * self.T + 1)
        self.engine.workspace['TEMPDIR'] = self.temp_dir
        if self.env_config['load_var'] == 'dynamic':
            self.engine.workspace['load_var'] = float(np.random.random() * 0.4 + 0.8)
        else:
            self.engine.workspace['load_var'] = float(self.env_config['load_var'])
        self.engine.Power_system_initialization(nargout=0, stdout=self.null_stream)

        self.q_history = [[] for _ in range(self.n)]

        return np.zeros(self.n * 2)

    def step(self, action: np.ndarray):  # -> observation, reward, done, info
        action = np.power(10, action)
        self.step_number += 1
        # self.progress_bar.set_description(f'{self.env_id}|{self.episode}|Running...')
        # self.progress_bar.update(1)
        try:
            var = self.engine.step(
                matlab.double(action[0 * self.n: 1 * self.n].reshape(self.n, 1).tolist()),  # \alpha
                matlab.double(action[1 * self.n: 2 * self.n].reshape(self.n, 1).tolist()),  # \beta
                matlab.double(action[2 * self.n: 3 * self.n].reshape(self.n, 1).tolist()),  # \gamma
                matlab.double(action[3 * self.n: 4 * self.n].reshape(self.n, 1).tolist()),  # \c
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

        for c in range(self.n):
            self.q_history[c].append(info['q'][c][0])
            if len(self.q_history[c]) > self.env_config['window_size']:
                del self.q_history[c][0]

        # q_average = np.mean(np.array(self.q_history), axis=1)
        obs = np.concatenate((info['v'].flatten(), info['q'].flatten()))
        # obs = info['v'].flatten()
        # self.prev_q = info['q'].flatten()

        # critical_voltage_met = np.all(np.abs(info['v'] - 1) < self.env_config['voltage_threshold'] * (
        #         1 + self.env_config['voltage_violation_critical_threshold']))
        #
        # voltages_converged = np.all(np.abs(info['v'] - 1) < self.env_config['voltage_threshold'])
        #
        voltage_deviations = np.mean(np.clip(np.abs(info['v'] - 1) - self.env_config['voltage_threshold'], 0, None))
        # changes = np.mean([np.mean(np.clip(
        #     np.abs(self.q_history[c][-1] - np.array(self.q_history[c])) / np.abs(self.q_history[c][-1]) - self.env_config[
        #         'change_threshold'], 0, None)) for c in range(self.n)])
        #
        # changes_converged = \
        #     len(self.q_history[0]) >= self.env_config['window_size'] and \
        #     all([np.all(
        #         np.abs(self.q_history[c][-1] - np.array(self.q_history[c])) / np.abs(self.q_history[c][-1]) < self.env_config[
        #             'change_threshold']) for c in range(self.n)])
        #
        # converged = voltages_converged and changes_converged
        #
        # info['changes'] = changes
        info['voltage_deviations'] = voltage_deviations

        done = self.step_number == self.T // self.env_config['repeat'] or (np.abs(info['q']) > 0.5).any()

        reward = 0

        # reward = .5 * (np.exp(-changes) - 1)\
        #        + .5 * (np.exp(-voltage_deviations) - 1)

        # reward += (np.exp(-voltage_deviations) - 1)
        # reward *= (1 - self.env_config['gamma'])

        if (np.abs(info['q']) > 0.5).any():
            reward -= 1

        return obs, reward, done, info

    def render(self, mode='human'):
        raise NotImplementedError()

    def close(self):
        if self.matlab_running is True:
            # self.progress_bar.close()
            self.matlab_running = False
            self.engine_pool.release(self.engine)
            self.logger.debug('Matlab closed.')
