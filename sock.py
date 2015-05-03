import functools
import socket
import select

from gevent import Greenlet, sleep


class ThrottledSocket(object):
    def __init__(self, socket, limit):
        self.limit = limit
        self.current = 0
        self.write_queue = []
        self.socket = socket
        self.write_loop = None
        self.rate_loop = None

    def _socket_writeable(self):
        select.select([], [self.socket], [])
        return True

    def _write_loop(self):
        while True:
            if self.current < self.limit:
                available_n = self.limit - self.current
            else:
                continue

            if self.socket_writable():
                bytes = self.queue.pop(available_n)
                socket.write(bytes)

                # TODO: Handle -> maybe the socket does not write all available_n.
                self._update_rate(available_n)

    def _rate_loop(self):
        while True:
            self.current = 0
            sleep(1)

    def _update_rate(self, n):
        self.current += n

        if self.rate_loop:
            self.rate_loop = Greenlet.spawn(functools.partial(self.rate_loop, self))

    def write(self, bytes):
        if not self.write_loop:
            self.write_loop = Greenlet.spawn(functools.partial(self.write_loop, self))

        self.write_queue.push(bytes)

    def read(self, nbytes=0):
        if self.current < self.limit:
            available_n = self.limit - self.current

            nbytes = nbytes if nbytes <= available_n else available_n

            return socket.read(nbytes)
        else:
            return None
