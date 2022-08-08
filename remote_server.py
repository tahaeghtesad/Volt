import logging
import socket
import sys
import time
from threading import Thread

import matlab.engine

from envs.power.malab_wrapper_alpha_gamma_single import MatlabWrapperAlphaGammaEnv
from envs.power.matlab_wrapper_single_param import MatlabWrapperEnvSingleParam
from util.env_util import Historitized
from util.network_util import Messenger
from util.reusable_pool import ReusablePool


class ServerThread(Thread):

    def __init__(self, env_id, messenger: Messenger, engine_pool: ReusablePool, **kwargs) -> None:
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.messenger = messenger
        self.finished = False
        self.env = None

        self.engine_pool = engine_pool

        self.env_id = env_id

    @staticmethod
    def init_matlab(i):
        start = time.time()
        logger = logging.getLogger(__name__)
        logger.debug(f'Starting MATLAB engine {i}...')
        engine = matlab.engine.start_matlab()
        logger.debug(f'MATLAB engine {i} started in {time.time() - start:.2f} seconds.')
        return engine

    @staticmethod
    def clean_matlab(engine):
        engine.quit()

    def run(self) -> None:
        self.logger.debug('Starting a remote environment...')
        info = messenger.get_message()
        self.logger.debug(f'Environment Config: {info["config"]}')
        assert info['event'] == 'start', 'Client Error.'

        self.env = Historitized(MatlabWrapperEnvSingleParam(self.env_id, self.engine_pool, info['config']), info['config']['history_size'])
        # self.env = Historitized(MatlabWrapperAlphaGammaEnv(self.env_id, self.engine_pool, info['config']), info['config']['history_size'])
        self.messenger.send_message(dict(observation_space=self.env.observation_space, action_space=self.env.action_space, n=self.env.env.n, T=self.env.env.T))

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
                    self.logger.debug('Connection closed.')
                    self.messenger.conn.close()
                    self.env.close()
                    self.finished = True
                elif message['event'] == 'exception':
                    if 'data' in message:
                        self.logger.exception(message['data'])
                    self.messenger.conn.close()
                    self.env.close()
                    self.finished = True
                    break

            except Exception as e:
                # Usully if there is an exception, the connection is closed. Therefore, the following line throws an exception.
                # self.messenger.send_message(dict(event='exception', data=str(e)))
                self.logger.exception(f'Client disconnected - {type(e)}')
                self.finished = True
                self.messenger.conn.close()
                self.env.close()
                break


if __name__ == '__main__':
    engine_pool = ReusablePool(12, ServerThread.init_matlab, ServerThread.clean_matlab)
    logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s', level=logging.INFO)
    port = int(sys.argv[1])
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind(('localhost', port))
    socket.listen(64)

    logging.info(f'Listening on port {port}')
    count = 0

    while True:
        conn, addr = socket.accept()
        logging.debug(f'Client Connected {addr}')
        messenger = Messenger(conn)

        try:
            thread = ServerThread(count, messenger, engine_pool)
            count += 1
            count %= 16
            thread.start()

        except ConnectionError:
            logging.error('Client disconnected.')
