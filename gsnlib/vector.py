from __future__ import annotations
import math
import numpy as np

EPS = 1E-16


class Vector(object):
    def __init__(self, x=0, y=0, z=0):
        if isinstance(x, list):
            self.v = np.array(x)
        else:
            self.v = np.array([x, y, z])

    @classmethod
    def from_array(cls, v):
        vec = cls()
        vec.v = np.array(v)
        return vec

    def __sub__(self, other: "Vector"):
        return self.__class__.from_array(self.v - other.v)

    def __lt__(self, other: "Vector"):
        return (self.x < other.x - EPS
                or (abs(self.x - other.x) < EPS and self.y < other.y - EPS))

    def dist(self, other: "Vector") -> float:
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

    def clone(self) -> Vector:
        return Vector(self.x, self.y)

    def negated(self) -> Vector:
        return Vector(-self.x, -self.y)

    def plus(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def minus(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y)

    def times(self, a: float) -> Vector:
        return Vector(self.x * a, self.y * a)

    def divide_by(self, a: float) -> Vector:
        return Vector(self.x / a, self.y / a)

    def dot(self, other: Vector) -> float:
        return self.x * other.x + self.y * other.y

    def lerp(self, other: Vector, t: float) -> Vector:
        return self.plus(other.minus(self).times(t))

    def length(self) -> float:
        return math.sqrt(self.dot(self))

    def unit(self) -> Vector:
        return self.divide_by(self.length())

    def squared_length_to(self, other: Vector) -> float:
        return ((self.x - other.x)
                * (self.x - other.x)
                + (self.y - other.y)
                * (self.y - other.y))

    def __eq__(self, o: Vector) -> bool:
        return self.x == o.x and self.y == o.y
