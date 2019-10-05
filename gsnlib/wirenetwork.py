from dataclasses import dataclass
from typing import List
from gsnlib.geometry import line_intersection
from gsnlib.geometry import Point


@dataclass
class Edge:
    a: int
    b: int


class WireNetwork(object):
    def __init__(self, tolerance=0.1):
        self._vertices: List[Point] = []
        self._edges: List[Edge] = []
        self.tolerance = tolerance

    def add_vertex(self, point: Point):
        for i, v in enumerate(self.vertices):
            if v.dist(point) < self.tolerance:
                return i

        self._vertices.append(point)
        return len(self._vertices) - 1

    def add_segment(self, p1, p2):
        # Loop through all existing points, checking
        # if new points already exists close
        # Then return indices or add new

        p1 = Point(p1)
        p2 = Point(p2)

        if p2 < p1:
            p1, p2 = p2, p1

        intersections = []
        new_edges = []
        clear = True
        for other in self._edges:
            p3, p4 = self._vertices[other.a], self._vertices[other.b]
            if p4 < p3:
                p3, p4 = p4, p3

            i = line_intersection(p1, p2, p3, p4)
            if i is not None:
                clear = False
                if type(i) == Point:
                    intersections.append((other, i))
                elif type(i) == tuple and len(i) == 2:
                    new_edge_length = p1.dist(p2)
                    prev_edge_length = p3.dist(p4)

                    if i[0].dist(i[1]) < self.tolerance:
                        intersections.append((other, i[0]))
                    elif ((p1.dist(i[0]) < self.tolerance and p2.dist(i[1]) < self.tolerance) or
                          (p3.dist(i[0]) < self.tolerance and p4.dist(i[1]) < self.tolerance)):

                        if new_edge_length > prev_edge_length:
                            p1_i = self.add_vertex(p1)
                            p2_i = self.add_vertex(p2)
                            new_edges.append(Edge(p1_i, other.a))
                            new_edges.append(Edge(other.b, p2_i))
                    else:
                        print("Overlap")
                        if p1.x < p3.x:
                            p1_i = self.add_vertex(p1)
                            p2_i = self.add_vertex(p2)
                            self._edges.remove(other)
                            new_edges.append(Edge(p1_i, other.a))
                            new_edges.append(Edge(other.a, p2_i))
                            new_edges.append(Edge(p2_i, other.b))
                        else:
                            p1_i = self.add_vertex(p1)
                            p2_i = self.add_vertex(p2)
                            self._edges.remove(other)
                            new_edges.append(Edge(other.a, p1_i))
                            new_edges.append(Edge(p1_i, other.b))
                            new_edges.append(Edge(other.b, p2_i))
                else:
                    raise Exception("WTF")

        if len(new_edges) > 0:
            for e in new_edges:
                self._edges.append(e)

        if len(intersections) > 0:
            print("Intersections: {}".format(len(intersections)))

            p1_i = self.add_vertex(p1)
            p2_i = self.add_vertex(p2)
            edge = Edge(p1_i, p2_i)

            px_i = []

            for other, p0 in intersections:
                self._edges.remove(other)
                p3_i = other.a
                p4_i = other.b
                p0_i = self.add_vertex(p0)
                px_i.append(p0_i)

                if p3_i != p0_i:
                    self._edges.append(Edge(p3_i, p0_i))

                if p4_i != p0_i:
                    self._edges.append(Edge(p4_i, p0_i))

            px_sorted = sorted(px_i,
                               key=lambda x: self._vertices[x].dist(self.vertices[p1_i]))

            prev_x = p1_i
            for px in px_sorted:
                if prev_x != px:
                    self._edges.append(Edge(prev_x, px))
                prev_x = px
            if prev_x != p2_i:
                self._edges.append(Edge(prev_x, p2_i))
            # self._edges.append(Edge(p1_i, p0_i))
            # self._edges.append(Edge(p2_i, p0_i))

        if clear:
            p1_i = self.add_vertex(p1)
            p2_i = self.add_vertex(p2)
            edge = Edge(p1_i, p2_i)

            self.edges.append(edge)

    @property
    def edges(self):
        return self._edges

    @property
    def vertices(self):
        return self._vertices
