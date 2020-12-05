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
