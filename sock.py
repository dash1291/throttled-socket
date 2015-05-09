import functools
import socket
import select

from gevent import Greenlet, sleep


class ThrottledSocket(object):
    def __init__(self, bind_socket, limit):
        self.limit = limit
        self.current = 0
        self.write_queue = ''
        self.socket = bind_socket
        self.write_loop = None
        self.rate_loop = None

    def _socket_writable(self):
        select.select([], [self.socket.fileno()], [])
        return True

    def _write_loop(self):
        while True:
            if self.current < self.limit:
                available_n = self.limit - self.current
            else:
                sleep(0)
                continue

            if self._socket_writable():
                bytes = self.write_queue[:available_n]
                self.write_queue = self.write_queue[available_n:]
                self.socket.send(bytes)

                # TODO: Handle -> maybe the socket does not write all available_n.
                self._update_rate(available_n)
            sleep(0)

    def _rate_loop(self):
        while True:
            self.current = 0
            sleep(1)

    def _update_rate(self, n):
        self.current += n

        if not self.rate_loop:
            self.rate_loop = Greenlet.spawn(self._rate_loop)

    def write(self, bytes):
        if not self.write_loop:
            self.write_loop = Greenlet.spawn(self._write_loop)

        self.write_queue += bytes

    def read(self, nbytes=0):
        if self.current < self.limit:
            available_n = self.limit - self.current

            nbytes = nbytes if nbytes <= available_n else available_n

            return socket.read(nbytes)
        else:
            return None
