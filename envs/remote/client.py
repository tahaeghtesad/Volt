import gym
import socket

import numpy as np

from util.network_util import Messenger


class RemoteEnv(gym.Env):

    def __init__(self, host, port):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((host, port))
        self.messenger = Messenger(conn)

        self.messenger.send_message(dict(env_params=dict()))

        env_info = self.messenger.get_message()
        self.action_space = env_info['action_space']
        self.observation_space = env_info['observation_space']

    def step(self, action):
        self.messenger.send_message({
            'event': 'step',
            'data': action
        })

        result = self.messenger.get_message()
        return result['obs'], result['reward'], result['done'], result['info']

    def reset(self):
        self.messenger.send_message({
            'event': 'reset'
        })

        result = self.messenger.get_message()
        return result['obs']

    def render(self, mode='human'):
        raise NotImplementedError()


if __name__ == '__main__':
    env = RemoteEnv('localhost', 6985)
    env.step(env.action_space.sample())