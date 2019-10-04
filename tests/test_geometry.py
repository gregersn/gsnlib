import unittest
from gsnlib.geometry import line_intersection, Point


class TestLineIntersection(unittest.TestCase):
    def test_intersection(self):
        i = line_intersection(Point([-10, -10]), Point([10, 10]),
                              Point([-10, 10]), Point([10, -10]))
        self.assertIsNotNone(i)
        self.assertAlmostEqual(i.x, 0)
        self.assertAlmostEqual(i.y, 0)

        i = line_intersection(Point([0, 2]), Point(
            [4, 2]), Point([2, 0]), Point([2, 4]))
        self.assertAlmostEqual(i.x, 2)
        self.assertAlmostEqual(i.y, 2)

        i = line_intersection(Point([0, 0]), Point(
            [10, 10]), Point([0, 2]), Point([10, 12]))
        self.assertIsNone(i)
