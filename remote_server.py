import logging
import socket
import sys
import time
from threading import Thread

from envs.power.thirteen_bus import ThirteenBus
from envs.power.thirteen_bus_single_param import SingleParamThirteenBus
from util.env_util import Historitized
from util.network_util import Messenger
from util.reusable_pool import ReusablePool

import matlab.engine


class ServerThread(Thread):

    def __init__(self, messenger: Messenger, engine_pool: ReusablePool, **kwargs) -> None:
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.messenger = messenger
        self.finished = False
        self.env = None

        self.engine_pool = engine_pool

    @staticmethod
    def init_matlab(i):
        start = time.time()
        logger = logging.getLogger(__name__)
        logger.info(f'Starting MATLAB engine {i}...')
        engine = matlab.engine.start_matlab()
        engine.addpath('C:\\Users\\Taha\\PycharmProjects\\Volt\\envs\\power\\matlab')
        logger.info(f'MATLAB engine {i} started in {time.time() - start:.2f} seconds.')
        return engine

    @staticmethod
    def clean_matlab(engine):
        engine.quit()

    def run(self) -> None:
        self.logger.info('Starting a remote environment...')
        info = messenger.get_message()
        self.logger.info(f'Environment Config: {info["config"]}')
        assert info['event'] == 'start', 'Client Error.'

        self.env = Historitized(SingleParamThirteenBus(self.engine_pool, info['config']), info['config']['history_size'])
        self.messenger.send_message(dict(observation_space=self.env.observation_space, action_space=self.env.action_space, n=1, T=self.env.env.T))

        while not self.finished:
            try:
                message = self.messenger.get_message()

                if message['event'] == 'step':
                    obs, reward, done, info = self.env.step(message['data'])
                    self.messenger.send_message(dict(obs=obs, reward=reward, done=done, info=info))

                elif message['event'] == 'reset':
                    obs = self.env.reset()
                    self.messenger.send_message(dict(obs=obs))

                elif message['event'] == 'close':
                    self.logger.info('Connection closed.')
                    self.messenger.conn.close()
                    self.env.close()
                    self.finished = True

            except Exception as e:
                self.logger.error(f'Client disconnected - {type(e)} - {e}')
                self.finished = True
                self.messenger.conn.close()
                self.env.close()


if __name__ == '__main__':
    engine_pool = ReusablePool(12, ServerThread.init_matlab, ServerThread.clean_matlab)
    logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s', level=logging.INFO)
    port = int(sys.argv[1])
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind(('localhost', port))
    socket.listen(64)

    logging.info(f'Listening on port {port}')

    while True:
        conn, addr = socket.accept()
        logging.info(f'Client Connected {addr}')
        messenger = Messenger(conn)

        try:
            thread = ServerThread(messenger, engine_pool)
            thread.start()

        except ConnectionError:
            logging.error('Client disconnected.')
