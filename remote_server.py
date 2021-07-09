import logging
import socket
import struct
import sys
from _thread import start_new_thread
from threading import Thread
from typing import Optional, Callable, Any, Iterable, Mapping
import json

from _socket import gethostbyname

from envs.power.single_node import SingleNode
from envs.power.thirteen_bus import ThirteenBus
from util.network_util import Messenger


class ServerThread(Thread):
    def __init__(self, messenger: Messenger, info: dict, **kwargs) -> None:
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.messenger = messenger
        self.info = info
        self.finished = False

    def run(self) -> None:
        self.env = SingleNode(0, self.info['env_params'])
        self.messenger.send_message(dict(observation_space=self.env.observation_space, action_space=self.env.action_space, n=1, T=self.env.T))

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

        except ConnectionError:
            self.logger.error(f'Client disconnected.')
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
            info = messenger.get_message()
            assert info['event'] == 'start'

            thread = ServerThread(messenger, info)
            thread.start()

        except ConnectionError:
            logging.error('Client disconnected.')