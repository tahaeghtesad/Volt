import socket
import struct
import sys
from _thread import start_new_thread
from threading import Thread
from typing import Optional, Callable, Any, Iterable, Mapping
import json

from _socket import gethostbyname

from envs.power.thirteen_bus import ThirteenBus
from util.network_util import Messenger


class ServerThread(Thread):
    def __init__(self, messenger: Messenger, env_params: dict, **kwargs) -> None:
        super().__init__(**kwargs)
        self.messenger = messenger
        self.env = ThirteenBus(env_params)

        self.messenger.send_message(dict(observation_space=self.env.observation_space, action_space=self.env.action_space))

    def run(self) -> None:
        try:
            while True:
                message = self.messenger.get_message()

                if message['event'] == 'step':
                    obs, reward, done, info = self.env.step(message['data'])
                    self.messenger.send_message(dict(obs=obs, reward=reward, done=done, info=info))

                if message['event'] == 'reset':
                    obs = self.env.reset()
                    self.messenger.send_message(dict(obs=obs))

                if message['event'] == 'close':
                    print('Connection closed.')
                    self.messenger.conn.close()
                    self.env.close()
                    break

        except ConnectionError:
            print(f'Client disconnected.')
            self.messenger.conn.close()
            self.env.close()


if __name__ == '__main__':
    port = int(sys.argv[1])
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind(('localhost', port))
    socket.listen(16)

    print(f'Listening on port {port}')

    while True:
        conn, addr = socket.accept()
        print(f'Client Connected {addr}')
        messenger = Messenger(conn)

        try:
            info = messenger.get_message()
            assert info['event'] == 'start'


            thread = ServerThread(messenger, info['env_params'])
            thread.start()

        except ConnectionError:
            print('Client disconnected.')