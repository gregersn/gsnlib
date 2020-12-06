from .line import Line
from ..vector import Vector
from typing import List


class Segment:
    def __init__(self, vertices: List[Vector], shared=None):
        self.vertices = vertices
        self.shared = shared
        self.line = Line.from_points(vertices[0], vertices[1])

    def __repr__(self):
        return f"<Segment ({self.vertices[0]}, {self.vertices[1]})>"

    def clone(self):
        vertices = [v.clone() for v in self.vertices]
        return self.__class__(vertices, self.shared)

    def flip(self):
        self.vertices.reverse()
        self.line.flip()

    def __eq__(self, o) -> bool:
        if len(self.vertices) != len(o.vertices):
            return False

        if self.shared is not None or o.shared is not None:
            if len(self.shared) != len(o.shared):
                return False

        if self.line != o.line:
            return False

        for i in range(len(self.vertices)):
            if self.vertices[i] != o.vertices[i]:
                return False

        if self.shared is not None:
            for i in range(len(self.shared)):
                if self.shared[i] != o.shared[i]:
                    return False

        return True
