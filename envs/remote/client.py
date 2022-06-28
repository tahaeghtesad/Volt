import logging
import multiprocessing
import socket

import gym

from util.network_util import Messenger


class RemoteEnv(gym.Env):

    def __init__(self, host, port, config):
        self.logger = logging.getLogger(__name__)
        self.host = host
        self.port = port
        self.config = config
        self.messenger = None

        self.step_number = 0
        self.epoch_number = 0
        self.__init_messenger()

    def __init_messenger(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((self.host, self.port))
        self.messenger = Messenger(conn)
        self.messenger.send_message(dict(event='start', config=self.config))

        env_info = self.messenger.get_message()
        self.action_space = env_info['action_space']
        self.observation_space = env_info['observation_space']
        self.T = env_info['T']
        self.n = env_info['n']

    def step(self, action):
        self.step_number += 1
        self.messenger.send_message(dict(event='step', data=action))

        result = self.messenger.get_message()
        return result['obs'], result['reward'], result['done'], result['info']

    def reset(self):
        self.step_number = 0
        self.epoch_number += 1

        # if self.epoch_number % 500 == 0:
        #     self.messenger.conn.close()
        #     self.__init_messenger()

        self.messenger.send_message(dict(event='reset'))

        result = self.messenger.get_message()
        return result['obs']

    def close(self):
        self.logger.info('Closing connection.')
        self.messenger.send_message(dict(event='close', data='Gracefully exiting.'))
        self.messenger.conn.close()

    def render(self, mode='human'):
        raise NotImplementedError()



def job(i):
    env = RemoteEnv('localhost', 6985, None)
    print(f'Starting {i}')
    env.reset()
    for step in range(500):
        env.step(env.action_space.sample())
    del env
    print(f'Done {i}')
    return True

if __name__ == '__main__':

    with multiprocessing.Pool(10) as p:
        p.map(job, range(1000))