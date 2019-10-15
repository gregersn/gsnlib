
import math
from .vector import Vector

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


def line_intersect_1d(a, b, c, d):
    if a > b:
        a, b = b, a
    if c > d:
        c, d = d, c

    return max(a, c) <= min(b, d) + EPS


def det(a, b, c, d):
    return a * d - b * c


def betw(l, r, x):
    return min(l, r) <= x + EPS and x <= max(l, r) + EPS


def line_intersection(a: Vector, b: Vector, c: Vector, d: Vector) -> Vector:
    if (not line_intersect_1d(a.x, b.x, c.x, d.x)
            or not line_intersect_1d(a.y, b.y, c.y, d.y)):
        return None

    m = Line(a, b)
    n = Line(c, d)

    zn = det(m.a, m.b, n.a, n.b)

    if (abs(zn) < EPS):
        if (abs(m.dist(c)) > EPS or abs(n.dist(a)) > EPS):
            return None

        if(b < a):
            a, b = b, a

        if(d < c):
            c, d = d, c

        left = max(a, c)
        right = min(b, d)
        return (left, right)
    else:
        x = -det(m.c, m.b, n.c, n.b) / zn
        y = -det(m.a, m.c, n.a, n.c) / zn
        if (betw(a.x, b.x, x) and betw(a.y, b.y, y) and
                betw(c.x, d.x, x) and betw(c.y, d.y, y)):
            return Vector([x, y])

    return None
