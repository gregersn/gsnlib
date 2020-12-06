import math
from ..vector import Vector
from gsnlib.constants import EPSILON


class Line(object):
    def __init__(self, p: Vector, q: Vector):
        self.a = p.y - q.y
        self.b = q.x - p.x
        self.c = -self.a * p.x - self.b * p.y
        self.norm()

    def norm(self):
        z = math.sqrt(self.a * self.a + self.b * self.b)
        if (abs(z) > EPSILON):
            self.a /= z
            self.b /= z
            self.c /= z

    def dist(self, p: Vector):
        return self.a * p.x + self.b * p.y + self.c
