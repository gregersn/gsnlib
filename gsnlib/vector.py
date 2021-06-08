from __future__ import annotations
import math
import numpy as np
from typing import List

from gsnlib.constants import EPSILON


class Vector:
    v: List[float]

    def __init__(self, x=0.0, y=0.0, z=0.0):
        if isinstance(x, list):
            self.v = np.array(x, dtype=np.float64)
        else:
            self.v = np.array([x, y, z], dtype=np.float64)

    @classmethod
    def from_array(cls, v):
        vec = cls()
        vec.v = np.array(v)
        return vec

    def __sub__(self, other: "Vector"):
        return self.__class__.from_array(self.v - other.v)

    def __lt__(self, other: "Vector"):
        return (self.x < other.x - EPSILON
                or (abs(self.x - other.x) < EPSILON
                    and self.y < other.y - EPSILON))

    def dist(self, other: "Vector") -> float:
        t = self - other
        return math.sqrt(t.x * t.x + t.y * t.y)

    def translate(self, x: float, y: float, z: float = 0):
        self.x += x
        self.y += y
        self.z += z

    def rotate(self, a):
        self.v[0:2] = self.v[0:2].dot(np.array([[np.cos(a), -np.sin(a)],
                                                [np.sin(a), np.cos(a)]]))

    @property
    def x(self) -> float:
        return self.v[0]

    @x.setter
    def x(self, x: float):
        self.v[0] = x

    @property
    def y(self) -> float:
        return self.v[1]

    @y.setter
    def y(self, y: float):
        self.v[1] = y

    @property
    def z(self) -> float:
        return self.v[2]

    @z.setter
    def z(self, z: float):
        self.v[2] = z

    def __repr__(self):
        if len(self.v) == 2:
            return "Vector({}, {})".format(*self.v)
        else:
            return "Vector({}, {}, {})".format(*self.v)

    def clone(self) -> Vector:
        return Vector(self.x, self.y)

    def copy(self) -> Vector:
        return self.clone()

    def negated(self) -> Vector:
        return Vector(-self.x, -self.y)

    def plus(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __add__(self, other: Vector) -> Vector:
        return self.plus(other)

    def minus(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y)

    def times(self, a: float) -> Vector:
        return Vector(self.x * a, self.y * a)

    def divide_by(self, a: float) -> Vector:
        return Vector(self.x / a, self.y / a)

    def __truediv__(self, a: float) -> Vector:
        return self.divide_by(a)

    def dot(self, other: Vector) -> float:
        return self.x * other.x + self.y * other.y

    def lerp(self, other: Vector, t: float) -> Vector:
        return self.plus(other.minus(self).times(t))

    def length(self) -> float:
        return math.sqrt(self.dot(self))

    def mag(self) -> float:
        return self.length()

    def magsq(self) -> float:
        return self.dot(self)

    def unit(self) -> Vector:
        return self.divide_by(self.length())

    def squared_length_to(self, other: Vector) -> float:
        return ((self.x - other.x)
                * (self.x - other.x)
                + (self.y - other.y)
                * (self.y - other.y))

    def __eq__(self, o: Vector) -> bool:
        return self.x == o.x and self.y == o.y

    def cross(self, other: Vector) -> Vector:
        return Vector(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)

    def normalize(self) -> Vector:
        return self / self.length()
