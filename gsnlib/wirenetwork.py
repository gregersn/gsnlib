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
        self._segment_queue = []

    def to_dict(self):
        return {
            'vertices': [[v.x, v.y] for v in self._vertices],
            'edges': [[e.a, e.b] for e in self._edges]
        }

    def from_dict(self, data):
        if 'edges' in data:
            self._edges = [Edge(e[0], e[1]) for e in data['edges']]

        if 'vertices' in data:
            self._vertices = [Point(v) for v in data['vertices']]

    def add_segment(self, p1, p2):
        self.add_to_segment_queue((Point(p1), Point(p2)))

        while len(self._segment_queue) > 0:
            p1, p2 = self._segment_queue.pop()
            self.add_edge(p1, p2)

    def add_to_segment_queue(self, seg):
        p1, p2 = seg

        if p2 < p1:
            p1, p2 = p2, p1

        # Check if points exists
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


    def add_vertex(self, point: Point, add=True):
        for i, v in enumerate(self.vertices):
            if v.dist(point) < self.tolerance:
                return i
    
        if add:
            self._vertices.append(point)
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

    def add_edge(self, p1, p2):
        # Loop through all existing points, checking
        # if new points already exists close
        # Then return indices or add new

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
                        # Most likely end-to-end
                        intersections.append((other, i[0]))

                    elif ((p1.dist(i[0]) < self.tolerance and p2.dist(i[1]) < self.tolerance) or
                          (p3.dist(i[0]) < self.tolerance and p4.dist(i[1]) < self.tolerance)):

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
            edge = Edge(p1_i, p2_i)

            px_i = []

            for other, p0 in intersections:
                self._edges.remove(other)
                p3_i = other.a
                p4_i = other.b
                p0_i = self.add_vertex(p0)
                px_i.append(p0_i)

                if p3_i != p0_i:
                    self._add_edge(Edge(p3_i, p0_i))

                if p4_i != p0_i:
                    self._add_edge(Edge(p4_i, p0_i))

            px_sorted = sorted(px_i,
                               key=lambda x: self._vertices[x].dist(self.vertices[p1_i]))

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
                if li is not None and type(li) == Point:
                    raise Exception(li)

    @property
    def edges(self):
        return self._edges

    @property
    def vertices(self):
        return self._vertices
