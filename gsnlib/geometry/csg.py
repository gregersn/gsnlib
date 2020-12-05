from __future__ import annotations

from ..vector import Vector
from .node import Node
from .segment import Segment
from typing import List


class CSG:
    def __init__(self, segments=List[Segment]):
        print("csg-constructor")
        self.segments: List[Segment] = segments

    @classmethod
    def from_segments(cls, segments=List[Segment]):
        print("csg-from-segments")
        csg = CSG()
        csg.segments = segments
        return csg

    @classmethod
    def from_polygons(cls, polygons: List[List[List[float]]]) -> CSG:
        print("csg-from-polygons")
        segments = []
        for i in range(len(polygons)):
            for j in range(len(polygons[i])):
                k = (j + 1) % (len(polygons[i]))
                segments.append(Segment([Vector(*polygons[i][j]),
                                         Vector(*polygons[i][k])]))

        return CSG(segments)

    @classmethod
    def from_vectors(cls, vectors: List[Vector]) -> CSG:
        """Assume nothing is repeated."""
        print("csg-from-vectors")
        segments = []
        for i in range(len(vectors)):
            j = (i + 1) % len(vectors)
            segments.append(Segment([vectors[i], vectors[j]]))

        return CSG(segments)

    def clone(self) -> CSG:
        print("csg-clone")
        csg = CSG()
        csg.segments = [p.clone() for p in self.segments]
        return csg

    def to_segments(self) -> List[Segment]:
        return self.segments

    def to_polygons(self):
        segments = self.to_segments()
        polygons = {}
        _list = segments.copy()

        def find_next(extremum):
            for i in range(len(_list)):
                if _list[i].vertices[0].squared_length_to(extremum) < 1:
                    result = _list[i].clone()
                    del _list[i]
                    return result

        current_index = 0
        while len(_list) > 0:
            polygons[current_index] = (polygons[current_index]
                                       if current_index < len(polygons)
                                       else [])

            if len(polygons[current_index]) == 0:
                polygons[current_index].append(_list[0].vertices[0])
                polygons[current_index].append(_list[0].vertices[1])
                _list.pop(0)
            next = find_next(polygons[current_index][len(polygons[current_index]) - 1])
            if next:
                polygons[current_index].append(next.vertices[1])
            else:
                current_index += 1

        return list(polygons.values())

    def union(self, other: CSG) -> CSG:
        a = Node(self.clone().segments)
        b = Node(other.clone().segments)

        a.invert()
        b.clip_to(a)
        b.invert()
        a.clip_to(b)
        b.clip_to(a)
        segs = b.all_segments()
        a.build(segs)
        a.invert()
        return CSG.from_segments(a.all_segments())

    def subtract(self, other: CSG) -> CSG:
        b = Node(self.clone().segments)
        a = Node(other.clone().segments)
        a.invert()
        a.clip_to(b)
        b.clip_to(a)
        b.invert()
        b.clip_to(a)
        b.invert()
        a.build(b.all_segments())
        a.invert()
        return CSG.from_segments(a.all_segments()).inverse()

    def intersect(self, other):
        a = Node(self.clone().segments)
        b = Node(other.clone().segments)
        a.clip_to(b)
        b.clip_to(a)
        b.invert()
        b.clip_to(a)
        b.invert()
        a.build(b.all_segments())
        return CSG.from_segments(a.all_segments())

    def inverse(self) -> CSG:
        csg = self.clone()
        for p in csg.segments:
            p.flip()
        return csg
