import unittest

from gsnlib import path
from gsnlib.vector import Vector


class TestPointLineDist(unittest.TestCase):
    def test_point_on_line(self):
        p = Vector(10, 10)
        p1 = Vector(0, 0)
        p2 = Vector(20, 20)

        dist = path.pointlinedist(p, p1, p2)

        self.assertAlmostEqual(dist, 0)

    def test_point_prependicular_to_end(self):
        p = Vector(10, 10)
        p1 = Vector(0, 0)
        p2 = Vector(0, 10)

        dist = path.pointlinedist(p, p1, p2)
        self.assertAlmostEqual(dist, 10)


class TestPointReduction(unittest.TestCase):
    def test_reduce_points_on_line(self):
        points = [
            Vector(0, 0),
            Vector(10, 10),
            Vector(20, 20)
        ]

        reduced = path.reduce_points(points, 0)

        self.assertEqual(len(reduced), 2)

    def test_reduce_points_off_line(self):
        points = [
            Vector(0, 0),
            Vector(10, 11),
            Vector(20, 20)
        ]

        reduced = path.reduce_points(points, 2)
        self.assertEqual(len(reduced), 2)
