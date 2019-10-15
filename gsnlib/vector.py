import math
import numpy as np

EPS = 1E-16


class Vector(object):
    def __init__(self, x=0, y=0, z=0):
        if type(x) == list:
            self.v = np.array(x)
        else:
            self.v = np.array([x, y, z])

    @classmethod
    def from_array(cls, v):
        vec = cls()
        vec.v = np.array(v)
        return vec

    def __sub__(self, other):
        return self.__class__.from_array(self.v - other.v)
    
    def __lt__(self, other):
        return (self.x < other.x - EPS
                or (abs(self.x - other.x) < EPS and self.y < other.y - EPS))
    
    def dist(self, other) -> float:
        t = self - other
        return math.sqrt(t.x * t.x + t.y * t.y)        

    def translate(self, x, y):
        pass

    def rotate(self, a):
        pass

    @property
    def x(self):
        return self.v[0]

    @property
    def y(self):
        return self.v[1]

    @property
    def z(self):
        return self.v[2]

    def __repr__(self):
        return "Vector({}, {}, {})".format(*self.v)
