import struct
import pickle


class Messenger:

    def __init__(self, conn) -> None:
        super().__init__()
        self.conn = conn

    def read_bytes(self, size):
        buff = b''
        while len(buff) < size:
            buff += self.conn.recv(size - len(buff))
        return buff

    def get_message(self):
        len = struct.unpack('!i', self.read_bytes(4))[0]
        message = pickle.loads(self.read_bytes(len))

        return message

    def send_message(self, message):
        buff = pickle.dumps(message)
        size = struct.pack('!i', len(buff))
        self.conn.send(size)
        self.conn.send(buff)
