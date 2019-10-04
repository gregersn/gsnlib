
import math

EPS = 1E-12


class Point(object):
    def __init__(self, d):
        self._d = d

    @property
    def x(self):
        return self._d[0]

    @property
    def y(self):
        return self._d[1]

    def __lt__(self, other):
        return (self.x < other.x - EPS
                or (abs(self.x - other.x) < EPS and self.y < other.y - EPS))

    def __repr__(self):
        return "Point: {}, {}".format(self.x, self.y)

    def __sub__(self, other):
        return Point([self.x - other.x, self.y - other.y])

    def dist(self, other) -> float:
        t = self - other
        return math.sqrt(t.x * t.x + t.y * t.y)


class Line(object):
    def __init__(self, p: Point, q: Point):
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

    def dist(self, p: Point):
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


def line_intersection(a: Point, b: Point, c: Point, d: Point) -> Point:
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
            return Point([x, y])

    return None
