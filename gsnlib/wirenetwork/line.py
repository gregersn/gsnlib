import math
from ..vector import Vector

EPS = 1E-12


class Line(object):
    def __init__(self, p: Vector, q: Vector):
        self.a = p.y - q.y
        self.b = q.x - p.x
        self.c = -self.a * p.x - self.b * p.y
        self.norm()

    def norm(self):
        z = math.sqrt(self.a * self.a + self.b * self.b)
        if (abs(z) > EPS):
            self.a /= z
            self.b /= z
            self.c /= z

    def dist(self, p: Vector):
        return self.a * p.x + self.b * p.y + self.c
