from typing import List
import numpy as np


class Coordinates(object):
    def __init__(self):
        self.matrix = np.identity(3)
        self.stack: List[np.ndarray] = []

    def reset(self):
        self.matrix = np.identity(3)
        self.stack = []

    def translate(self, x: float, y: float):
        m = np.identity(3)
        m[0, 2] = x
        m[1, 2] = y
        self.matrix = self.matrix.dot(m)

    def rotate(self, v: float):
        r = np.identity(3)
        r[0, 0] = np.cos(v)
        r[0, 1] = -np.sin(v)
        r[1, 0] = np.sin(v)
        r[1, 1] = np.cos(v)
        self.matrix = self.matrix.dot(r)

    def scale(self, v: float):
        s = np.identity(3)
        s[0, 0] = v
        s[1, 1] = v
        self.matrix = self.matrix.dot(s)

    def push(self):
        self.stack.append(self.matrix.copy())

    def pop(self):
        self.matrix = self.stack.pop()

    @property
    def pos(self):
        pos = np.array([0, 0, 1])
        return self.matrix.dot(pos).round(3)[0:2]

    @property
    def pos3d(self):
        return np.append(self.pos, 0)

    @property
    def x(self) -> float:
        return self.pos[0]

    @property
    def y(self) -> float:
        return self.pos[1]
