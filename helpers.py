import time
import numpy as np


def curr_ts_ms():
    return int(time.time() * 1000)


class RingBuffer(object):
    def __init__(self, length):
        self.length = length
        self.data = np.zeros(length)
        self.index = 0
        self.real_length = 0

    def append(self, x):
        self.data[self.index] = x
        self.index = (self.index + 1) % self.length
        if self.real_length < self.length:
            self.real_length += 1

    def get(self):
        idx = (self.index + np.arange(self.length)) % self.length
        return self.data[idx]

    def get_real(self):
        idx = (self.index - self.real_length
               + np.arange(self.real_length)) % self.length
        return self.data[idx]

    def reset(self):
        self.data.fill(0)
        self.index = 0


class TimeoutError(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutError()
