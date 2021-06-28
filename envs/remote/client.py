import gym
import socket

import numpy as np

from util.network_util import Messenger


class RemoteEnv(gym.Env):

    def __init__(self, host, port, config):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((host, port))
        self.messenger = Messenger(conn)

        self.messenger.send_message(dict(env_params=dict(event='start')))

        env_info = self.messenger.get_message()
        self.action_space = env_info['action_space']
        self.observation_space = env_info['observation_space']

    def step(self, action):
        self.messenger.send_message(dict(event='step', data=action))

        result = self.messenger.get_message()
        return result['obs'], result['reward'], result['done'], result['info']

    def reset(self):
        self.messenger.send_message(dict(event='reset'))

        result = self.messenger.get_message()
        return result['obs']

    def close(self):
        self.messenger.send_message(dict(event='close'))
        self.messenger.conn.close()

    def __del__(self):
        self.close()

    def render(self, mode='human'):
        raise NotImplementedError()


if __name__ == '__main__':
    env = RemoteEnv('localhost', 6985, None)
    env.reset()
    env.step(env.action_space.sample())