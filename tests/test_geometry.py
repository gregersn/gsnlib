import unittest
from gsnlib.geometry import line_intersection
from gsnlib.vector import Vector


class TestLineIntersection(unittest.TestCase):
    def test_intersection(self):
        i = line_intersection(Vector([10, 10]), Vector([-10, -10]),
                              Vector([10, -10]), Vector([-10, 10]))
        self.assertIsNotNone(i)
        self.assertIsInstance(i, Vector)

        if isinstance(i, Vector):
            self.assertAlmostEqual(i.x, 0)
            self.assertAlmostEqual(i.y, 0)

        i = line_intersection(Vector([0, 2]), Vector(
            [4, 2]), Vector([2, 0]), Vector([2, 4]))

        if isinstance(i, Vector):
            self.assertAlmostEqual(i.x, 2)
            self.assertAlmostEqual(i.y, 2)

        i = line_intersection(Vector([0, 0]), Vector(
            [10, 10]), Vector([0, 2]), Vector([10, 12]))
        self.assertIsNone(i)
