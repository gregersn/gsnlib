from __future__ import annotations

from ..vector import Vector
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from .segment import Segment

from gsnlib.geometry import segment as s

EPSILON = 1e-5


class Line():
    def __init__(self, origin: Vector, direction: Vector):
        self.origin = origin
        self.direction = direction
        self.normal = Vector(self.direction.y, -self.direction.x)

    def __eq__(self, o: Line) -> bool:
        return (self.origin == o.origin
                and self.direction == o.direction
                and self.normal == o.normal)

    def __repr__(self):
        return f"<Line({self.origin}, {self.direction}>"

    @classmethod
    def from_points(cls, a: Vector, b: Vector) -> Line:
        dir = b.minus(a).unit()
        return cls(a, dir)

    def clone(self) -> Line:
        print("line-clone")
        return Line(self.origin.clone(), self.direction.clone())

    def flip(self):
        self.direction = self.direction.negated()
        self.normal = self.normal.negated()

    def split_segment(self, segment: Segment,
                      colinear_right: List[Segment],
                      colinear_left: List[Segment],
                      right: List[Segment],
                      left: List[Segment]):
        print("line-split_segment")
        COLINEAR = 0
        RIGHT = 1
        LEFT = 2
        SPANNING = 3

        segment_type = 0
        types = []
        t = None
        for i in range(len(segment.vertices)):
            t = self.normal.dot(segment.vertices[i].minus(self.origin))
            type = COLINEAR
            if (t < -EPSILON):
                type = RIGHT
            elif (t > EPSILON):
                type = LEFT
            segment_type |= type
            types.append(type)

        if segment_type == COLINEAR:
            print("COLINEAR")
            if t != 0:
                if t > 0:
                    colinear_right.append(segment)
                else:
                    colinear_left.append(segment)
            else:
                if segment.line.origin.x < self.origin.x:
                    colinear_left.append(segment)
                else:
                    colinear_right.append(segment)

        elif segment_type == RIGHT:
            print("RIGHT")
            right.append(segment)
        elif segment_type == LEFT:
            print("LEFT")
            left.append(segment)
        elif segment_type == SPANNING:
            new_right = []
            new_left = []

            ti = types[0]
            tj = types[1]

            vi = segment.vertices[0]
            vj = segment.vertices[1]

            if ti == RIGHT and tj == RIGHT:
                new_right.append(vi)
                new_right.append(vj)

            if ti == LEFT and tj == LEFT:
                new_left.append(vi)
                new_left.append(vj)

            if ti == RIGHT and tj == LEFT:
                t = self.normal.dot(self.origin.minus(vi)) / self.normal.dot(vj.minus(vi))
                v = vi.lerp(vj, t)
                new_right.append(vi)
                new_right.append(v)
                new_left.append(v.clone())
                new_left.append(vj)

            if ti == LEFT and tj == RIGHT:
                t = self.normal.dot(self.origin.minus(vi)) / self.normal.dot(vj.minus(vi))
                v = vi.lerp(vj, t)
                new_left.append(vi)
                new_left.append(v)
                new_right.append(v.clone())
                new_right.append(vj)

            if len(new_right) >= 2:
                right.append(s.Segment(new_right, segment.shared))

            if len(new_left) >= 2:
                left.append(s.Segment(new_left, segment.shared))
        else:
            raise UnboundLocalError
