import time
import numpy as np
import select


READ_FLAGS = select.POLLIN | select.POLLPRI
WRITE_FLAGS = select.POLLOUT
ERR_FLAGS = select.POLLERR | select.POLLHUP | select.POLLNVAL
ALL_FLAGS = READ_FLAGS | WRITE_FLAGS | ERR_FLAGS


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


class MeanVarHistory(object):
    def __init__(self):
        self.length = 0
        self.mean = 0.0
        self.square_mean = 0.0
        self.var = self.square_mean - np.square(self.mean)

    def append(self, x):
        length_new = self.length + len(x)
        ratio_old = float(self.length) / length_new
        ratio_new = float(len(x)) / length_new

        self.length = length_new
        self.mean = self.mean * ratio_old + np.mean(x) * ratio_new
        self.square_mean = (self.square_mean * ratio_old +
                            np.mean(np.square(x)) * ratio_new)
        self.var = self.square_mean - np.square(self.mean)

    def get_mean_var(self):
        return self.mean, self.var
