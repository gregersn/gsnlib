from typing import List
from ..vector import Vector  # noqa
from .node import Node  # noqa
from .segment import Segment  # noqa
from .line import Line  # noqa
from .csg import CSG  # noqa


class Polygon():
    points: List[Vector]

    def __init__(self, points: List[Vector] = []):
        self.points = points

    def contains(self, pt: Vector) -> bool:
        if len(self.points) != 3:
            raise NotImplementedError("Not implmented for more than 3 points")
        v1, v2, v3 = self.points

        d1 = self.sign(pt, v1, v2)
        d2 = self.sign(pt, v2, v3)
        d3 = self.sign(pt, v3, v1)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    def sign(self, p1: Vector, p2: Vector, p3: Vector):
        return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

    def area(self):
        prev_point = self.points[-1]
        area = 0
        for point in self.points:
            area += prev_point.x * point.y - point.x * prev_point.y
            prev_point = point

        return area / 2.0

    def winding(self):
        return -1 if self.area() < 0 else 1

    def segments(self):
        for idx, cur in enumerate(self.points):
            next = self.points[(idx + 1) % len(self.points)]
            yield Segment([cur, next])

    def __repr__(self):
        return f"Vector({[p for p in self.points]}>"


class Shape():
    polygons: List[Polygon]

    def __init__(self, polygons: List[Polygon]):
        self.polygons = polygons


def ray_segment_intersection(ray: Line, segment: Segment):
    def cross(a: Vector, b: Vector) -> float:
        return a.x * b.y - a.y * b.x

    p = ray.origin
    r = ray.direction

    q = segment.start
    s = segment.end - q

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

        if t >= 0 and u >= 0 and u <= 1:
            return p + r.times(t)
