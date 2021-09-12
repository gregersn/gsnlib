from dataclasses import dataclass
from typing import Any, Callable, Dict, List, TypedDict, Union
from gsnlib.vector import Vector
from .line import Line
from typing import Tuple

from gsnlib.constants import EPSILON

SegmentType = Tuple[Vector, Vector]


def line_intersect_1d(a: float, b: float, c: float, d: float):
    if a > b:
        a, b = b, a
    if c > d:
        c, d = d, c

    return max(a, c) <= min(b, d) + EPSILON


def det(a: float, b: float, c: float, d: float):
    return a * d - b * c


def betw(left:  float, right: float, x: float):
    return min(left, right) <= x + EPSILON and x <= max(left, right) + EPSILON


def line_intersection(a: Vector,
                      b: Vector,
                      c: Vector,
                      d: Vector) -> Union[SegmentType, Vector, None]:
    if (not line_intersect_1d(a.x, b.x, c.x, d.x)
            or not line_intersect_1d(a.y, b.y, c.y, d.y)):
        return None

    m = Line(a, b)
    n = Line(c, d)

    zn = det(m.a, m.b, n.a, n.b)

    if (abs(zn) < EPSILON):
        if (abs(m.dist(c)) > EPSILON or abs(n.dist(a)) > EPSILON):
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


@dataclass
class Edge:
    a: int
    b: int


class NetworkData(TypedDict, total=False):
    edges: List[Tuple[int, int]]
    vertices: List[List[float]]


class WireNetwork:
    _segment_queue: List[SegmentType]

    def __init__(self, tolerance: float = 0.1):
        self._vertices: List[Vector] = []
        self._edges: List[Edge] = []
        self.tolerance = tolerance
        self._segment_queue = []

    def to_dict(self):
        return {
            'vertices': [[v.x, v.y] for v in self._vertices],
            'edges': [[e.a, e.b] for e in self._edges]
        }

    def from_dict(self, data: NetworkData):
        if 'edges' in data:
            self._edges = [Edge(e[0], e[1]) for e in data['edges']]

        if 'vertices' in data:
            self._vertices = [Vector(v) for v in data['vertices']]

    def add_segment(self, p1: List[float], p2: List[float]):
        self.add_to_segment_queue((Vector.from_array(p1),
                                   Vector.from_array(p2)))

        while len(self._segment_queue) > 0:
            _p1, _p2 = self._segment_queue.pop()
            self.add_edge(_p1, _p2)

    def add_to_segment_queue(self, seg: SegmentType):
        p1, p2 = seg

        if p2 < p1:
            p1, p2 = p2, p1

        # Check if Vectors exists
        p1_i = self.add_vertex(seg[0], add=False)
        p2_i = self.add_vertex(seg[1], add=False)

        # Check if segment exists
        if p1_i is not None and p2_i is not None:
            for s in self._edges:
                if s == Edge(p1_i, p2_i):
                    return

        # Check length of segment
        if p1.dist(p2) < self.tolerance:
            return

        # Check if segment already in queue
        for s in self._segment_queue:
            if s == seg:
                return

        # Add segment to queue
        self._segment_queue.append(seg)

    def add_vertex(self, Vector: Vector, add: bool = True) -> Union[int, None]:
        for i, v in enumerate(self.vertices):
            if v.dist(Vector) < self.tolerance:
                return i

        if add:
            self._vertices.append(Vector)
            return len(self._vertices) - 1
        else:
            return None

    def _add_edge(self, e: Edge):
        for other in self._edges:
            if e.a == other.a and e.b == other.b:
                return
            if e.a == other.b and e.b == other.a:
                return
        self._edges.append(e)

    def add_edge(self, p1: Vector, p2: Vector):
        # Loop through all existing Vectors, checking
        # if new Vectors already exists close
        # Then return indices or add new

        if p2 < p1:
            p1, p2 = p2, p1

        intersections: List[Tuple[Edge, Vector]] = []
        new_edges: List[Any] = []
        clear = True
        for other in self._edges:
            p3, p4 = self._vertices[other.a], self._vertices[other.b]
            if p4 < p3:
                p3, p4 = p4, p3

            i = line_intersection(p1, p2, p3, p4)

            if i is not None:
                clear = False
                if isinstance(i, Vector):
                    intersections.append((other, i))
                elif len(i) == 2:
                    new_edge_length = p1.dist(p2)
                    prev_edge_length = p3.dist(p4)

                    if i[0].dist(i[1]) < self.tolerance:
                        # Most likely end-to-end
                        intersections.append((other, i[0]))

                    elif ((p1.dist(i[0]) < self.tolerance
                           and p2.dist(i[1]) < self.tolerance) or
                          (p3.dist(i[0]) < self.tolerance
                           and p4.dist(i[1]) < self.tolerance)):

                        # This is one contained inside the other
                        if new_edge_length > prev_edge_length:
                            p3 = self._vertices[other.a]
                            p4 = self._vertices[other.b]
                            if p4 < p3:
                                p3, p4 = p4, p3
                            if p2 < p1:
                                p1, p2 = p2, p1
                            self.add_to_segment_queue(
                                (p1, p3))
                            self.add_to_segment_queue(
                                (p4, p2))
                    else:
                        # Overlap
                        if p1.x < p3.x:
                            self._edges.remove(other)
                            self.add_to_segment_queue(
                                (p1, self._vertices[other.a]))
                            self.add_to_segment_queue(
                                (self._vertices[other.a], p2))
                            self.add_to_segment_queue(
                                (p2, self._vertices[other.b]))
                        else:
                            self._edges.remove(other)
                            self.add_to_segment_queue(
                                (self._vertices[other.a], p1))
                            self.add_to_segment_queue(
                                (p1, self._vertices[other.b]))
                            self.add_to_segment_queue(
                                (self._vertices[other.b], p2))
                else:
                    raise Exception("WTF")

        if len(new_edges) > 0:
            for e in new_edges:
                self._add_edge(e)

        if len(intersections) > 0:
            p1_i = self.add_vertex(p1)
            p2_i = self.add_vertex(p2)
            if p1_i is None or p2_i is None:
                return
            edge = Edge(p1_i, p2_i)

            px_i: List[int] = []

            for other, p0 in intersections:
                self._edges.remove(other)
                p3_i = other.a
                p4_i = other.b
                p0_i = self.add_vertex(p0)
                if p0_i is not None:
                    px_i.append(p0_i)

                if p3_i != p0_i and p0_i is not None:
                    self._add_edge(Edge(p3_i, p0_i))

                if p4_i != p0_i and p0_i is not None:
                    self._add_edge(Edge(p4_i, p0_i))

            sort_key: Callable[[int], float] = lambda x: self._vertices[x].dist(
                self.vertices[p1_i if p1_i is not None else x])
            px_sorted = sorted(px_i, key=sort_key)

            prev_x = p1_i
            for px in px_sorted:
                if prev_x != px:
                    self._add_edge(Edge(prev_x, px))
                prev_x = px
            if prev_x != p2_i:
                self._add_edge(Edge(prev_x, p2_i))

        if clear:
            p1_i = self.add_vertex(p1)
            p2_i = self.add_vertex(p2)
            if p2_i is None or p1_i is None:
                return

            edge = Edge(p1_i, p2_i)

            self._add_edge(edge)

    def check_edges(self):
        for edge_a in self.edges:
            for edge_b in self.edges[1:]:
                p1 = self._vertices[edge_a.a]
                p2 = self._vertices[edge_a.b]
                p3 = self._vertices[edge_b.a]
                p4 = self._vertices[edge_b.b]

                li = line_intersection(p1, p2, p3, p4)
                if li is not None and type(li) == Vector:
                    raise Exception(li)

    @property
    def edges(self):
        return self._edges

    @property
    def vertices(self):
        return self._vertices
