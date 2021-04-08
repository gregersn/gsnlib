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


class Shape():
    polygons: List[Polygon]

    def __init__(self, polygons: List[Polygon]):
        self.polygons = polygons
