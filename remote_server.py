import logging
import socket
import sys
from threading import Thread

from envs.power.single_node import SingleNode
from util.env_util import Historitized
from util.network_util import Messenger


class ServerThread(Thread):
    def __init__(self, messenger: Messenger, **kwargs) -> None:
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.messenger = messenger
        self.finished = False
        self.env = None

    def run(self) -> None:
        self.logger.info('Starting a remote environment...')
        info = messenger.get_message()
        assert info['event'] == 'start', 'Client Error.'

        self.env = Historitized(SingleNode(info['config']), info['config']['history_size'])
        self.messenger.send_message(dict(observation_space=self.env.observation_space, action_space=self.env.action_space, n=1, T=self.env.env.T))

        try:
            while not self.finished:
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
            thread = ServerThread(messenger)
            thread.start()

        except ConnectionError:
            logging.error('Client disconnected.')
