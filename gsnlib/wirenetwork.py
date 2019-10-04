from dataclasses import dataclass
from typing import List
from gsnlib.geometry import line_intersection
from gsnlib.geometry import Point


@dataclass
class Edge:
    a: int
    b: int


class WireNetwork(object):
    def __init__(self):
        self._vertices: List(Point) = []
        self._edges: List[Edge] = []
        self.tolerance = 0.1

    def add_segment(self, p0, p1):
        # Loop through all existing points, checking
        # if new points already exists close
        # Then return indices or add new

        p0 = Point(p0)
        p1 = Point(p1)

        p0_i = None
        p1_i = None

        for i, v in enumerate(self.vertices):
            if v.dist(p0) < self.tolerance:
                p0_i = i

            if v.dist(p1) < self.tolerance:
                p1_i = i

        if p0_i is None:
            self._vertices.append(p0)
            p0_i = len(self._vertices) - 1

        if p1_i is None:
            self._vertices.append(p1)
            p1_i = len(self._vertices) - 1

        self.add_edge(Edge(p0_i, p1_i))

    def add_edge(self, edge: Edge):
        p1, p2 = self._vertices[edge.a], self._vertices[edge.b]
        intersections = []
        for other in self._edges:
            p3, p4 = self._vertices[other.a], self._vertices[other.b]

            i = line_intersection(p1, p2, p3, p4)
            if i is not None:
                intersections.append((other, i))

        if len(intersections) > 0:
            print("Intersections: {}".format(len(intersections)))

            p1_i = edge.a
            p2_i = edge.b

            px_i = []

            for other, p0 in intersections:
                self._edges.remove(other)
                p3_i = other.a
                p4_i = other.b
                self._vertices.append(p0)
                p0_i = len(self._vertices) - 1
                px_i.append(p0_i)

                self._edges.append(Edge(p3_i, p0_i))
                self._edges.append(Edge(p4_i, p0_i))

            px_sorted = sorted(px_i,
                               key=lambda x: self._vertices[x].dist(self.vertices[p1_i]))

            prev_x = p1_i
            for px in px_sorted:
                self._edges.append(Edge(prev_x, px))
                prev_x = px
            self._edges.append(Edge(prev_x, p2_i))
            # self._edges.append(Edge(p1_i, p0_i))
            # self._edges.append(Edge(p2_i, p0_i))

        else:
            self.edges.append(edge)

    @property
    def edges(self):
        return self._edges

    @property
    def vertices(self):
        return self._vertices
