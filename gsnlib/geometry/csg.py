from gsnlib.constants import EPSILON

import logging
from ..vector import Vector
from .node import Node
from .segment import Segment
from typing import Dict, List, Union


logger = logging.getLogger(__file__)

PolygonList = List[List[Union[List[float], Vector]]]


class CSG:
    def __init__(self, segments: List[Segment] = []):
        logger.debug("csg-constructor")
        self.segments: List[Segment] = segments

    @classmethod
    def from_segments(cls, segments: List[Segment]):
        logger.debug("csg-from-segments")
        csg = CSG()
        csg.segments = segments
        return csg

    @classmethod
    def from_polygons(cls,
                      polygons: PolygonList) -> 'CSG':
        logger.debug("csg-from-polygons")
        segments: List[Segment] = []
        for i in range(len(polygons)):
            for j in range(len(polygons[i])):
                k = (j + 1) % (len(polygons[i]))
                a = polygons[i][j]
                b = polygons[i][k]
                if isinstance(a, Vector) and isinstance(b, Vector):
                    segments.append(Segment([a, b]))
                elif isinstance(a, list) and isinstance(b, list):
                    segments.append(Segment([Vector(*a),
                                             Vector(*b)]))

        return CSG(segments)

    @classmethod
    def from_vectors(cls, vectors: List[Vector]) -> 'CSG':
        """Assume nothing is repeated."""
        logger.debug("csg-from-vectors")
        segments: List[Segment] = []
        for i in range(len(vectors)):
            j = (i + 1) % len(vectors)
            segments.append(Segment([vectors[i], vectors[j]]))

        return CSG(segments)

    def clone(self) -> 'CSG':
        logger.debug("csg-clone")
        csg = CSG()
        csg.segments = [p.clone() for p in self.segments]
        return csg

    def to_segments(self) -> List[Segment]:
        return self.segments

    def to_polygons(self) -> List[List[Vector]]:
        segments = self.to_segments()
        polygons: Dict[int, List[Vector]] = {}
        _list = segments.copy()

        def find_next(extremum: Vector):
            for i in range(len(_list)):
                if _list[i].vertices[0].squared_length_to(extremum) < EPSILON:
                    result = _list[i].clone()
                    del _list[i]
                    return result

        current_index = 0
        while len(_list) > 0:
            polygons[current_index] = (polygons[current_index]
                                       if current_index < len(polygons.keys())
                                       else [])

            if len(polygons[current_index]) == 0:
                polygons[current_index].append(_list[0].vertices[0])
                polygons[current_index].append(_list[0].vertices[1])
                _list.pop(0)
            extremum = polygons[current_index][len(
                polygons[current_index]) - 1]
            next = find_next(extremum)
            if next:
                polygons[current_index].append(next.vertices[1])
            else:
                current_index += 1

        return list(polygons.values())

    def union(self, other: 'CSG') -> 'CSG':
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

    def subtract(self, other: 'CSG') -> 'CSG':
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

    def intersect(self, other: 'CSG'):
        a = Node(self.clone().segments)
        b = Node(other.clone().segments)
        a.clip_to(b)
        b.clip_to(a)
        b.invert()
        b.clip_to(a)
        b.invert()
        a.build(b.all_segments())
        return CSG.from_segments(a.all_segments())

    def inverse(self) -> 'CSG':
        csg = self.clone()
        for p in csg.segments:
            p.flip()
        return csg
