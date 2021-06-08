from .line import Line
from ..vector import Vector
from typing import List


class Segment:
    def __init__(self, vertices: List[Vector], shared=None):
        self.vertices = vertices
        self.shared = shared
        self.line = Line.from_points(vertices[0], vertices[1])

    def __repr__(self):
        return f"<Segment ({self.vertices[0]}, {self.vertices[1]})>"

    def clone(self):
        vertices = [v.clone() for v in self.vertices]
        return self.__class__(vertices, self.shared)

    def flip(self):
        self.vertices.reverse()
        self.line.flip()

    def __eq__(self, o) -> bool:
        if len(self.vertices) != len(o.vertices):
            return False

        if self.shared is not None or o.shared is not None:
            if len(self.shared) != len(o.shared):
                return False

        if self.line != o.line:
            return False

        for i in range(len(self.vertices)):
            if self.vertices[i] != o.vertices[i]:
                return False

        if self.shared is not None:
            for i in range(len(self.shared)):
                if self.shared[i] != o.shared[i]:
                    return False

        return True

    @property
    def start(self):
        return self.vertices[0]

    @property
    def end(self):
        return self.vertices[-1]

    def intersect(self, other: 'Segment'):
        # v x w = vx * wy - vy * wx
        # p -> p + r and q -> q + s
        # p + tr and q + us
        # intersect if p + tr == q + us for t and u

        # cross both sides with s
        # (p + tr) x s = (q + us) x s
        # # s x s = 0
        # t ( r x s) = (q - p) x s
        # t = (q - p) x s / (r x s)

        def cross(a: Vector, b: Vector) -> float:
            return a.x * b.y - a.y * b.x

        p = self.start
        r = self.end - p

        q = other.start
        s = other.end - q

        rxs = cross(r, s)

        qsubp = q - p

        qsubpXr = cross(qsubp, r)
        qsubpXs = cross(qsubp, s)

        if rxs == 0 and qsubpXr == 0:
            # TODO: Colinear, find out if they are overlapping
            # or not
            return None

        if rxs == 0 and qsubpXr != 0:
            # Lines are parallell and non-intersecting
            return None

        if rxs != 0:
            t = qsubpXs / rxs
            u = qsubpXr / rxs

            if t >= 0 and t <= 1 and u >= 0 and u <= 1:
                return p + r.times(t)
