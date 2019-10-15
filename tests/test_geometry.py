import random
import unittest
from gsnlib.geometry import line_intersection, Point


class TestPoint(unittest.TestCase):
    def test_repr(self):
        p = Point([0, 0])
        self.assertEqual(repr(p), "Point([0, 0])")

        p = Point([-4, 3])
        self.assertEqual(repr(p), "Point([-4, 3])")
    
    def test_properties(self):
        a = random.random()
        b = random.random()

        p = Point([a, b])

        self.assertAlmostEqual(p.x, a)
        self.assertAlmostEqual(p.y, b)

    def test_lt(self):
        a = Point([0, 0])
        b = Point([-1, 0])

        self.assertTrue(b < a)
        self.assertFalse(a < b)

    def test_sub(self):
        a = Point([0, 0])
        b = Point([-1, 0])

        c = a - b
        self.assertEqual(c.x, 1)
        self.assertEqual(c.y, 0)

    def test_dist(self):
        a = Point([0, 0])
        b = Point([3, 4])
        self.assertEqual(a.dist(b), 5)


class TestLineIntersection(unittest.TestCase):
    def test_intersection(self):
        i = line_intersection(Point([10, 10]), Point([-10, -10]),
                              Point([10, -10]), Point([-10, 10]))
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
