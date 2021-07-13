import struct
import pickle


class Messenger:

    def __init__(self, conn) -> None:
        super().__init__()
        self.conn = conn
        # self.conn.settimeout(30)

    def read_bytes(self, size):
        buff = b''
        while len(buff) < size:
            recv = self.conn.recv(size - len(buff))
            if recv == b'':
                raise ConnectionError('Socket Broken.')
            buff += recv
        return buff

    def get_message(self):
        len = struct.unpack('!i', self.read_bytes(4))[0]
        message = pickle.loads(self.read_bytes(len))

        return message

    def send_message(self, message):
        buff = pickle.dumps(message)
        size = struct.pack('!i', len(buff))
        count =  self.conn.send(size)
        count += self.conn.send(buff)

        if count == 0:
            raise ConnectionError('Socket Broken.')
