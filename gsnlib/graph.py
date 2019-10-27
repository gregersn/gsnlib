from typing import List


class Vertex(object):
    pass


class Edge(object):
    def __init__(self, a: int, b: int, directed=False):
        self.a = a
        self.b = b

    @property
    def loop(self):
        return self.a == self.b

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

    def __lt__(self, other):
        if self.a < other.a:
            return True

        if self.a == other.a:
            if self.b < other.b:
                return True

        return False


class Graph(object):
    def __init__(self, directed=False):
        self.directed: bool = directed
        self.vertices: List(Vertex) = []
        self.edges: List(Edge) = []

    @property
    def simple(self) -> bool:
        return not self.loops and not self.multiples

    @property
    def loops(self) -> bool:
        for edge in self.edges:
            if edge.loop:
                return True

        return False

    @property
    def multiples(self) -> bool:
        if len(self.edges) < 1:
            return False

        s = sorted(self.edges)
        e0 = s[0]
        for e in s[1:]:
            if e0 == e:
                return True
            e0 = e
        return False

    def add_edge(self, a: int, b: int):
        if not self.directed and b < a:
            a, b = b, a
        self.edges.append(Edge(a, b))
