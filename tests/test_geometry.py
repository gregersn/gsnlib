from typing import Tuple
import unittest
from gsnlib.wirenetwork import line_intersection
from gsnlib.vector import Vector
from gsnlib.geometry import Segment, Line, ray_segment_intersection


class TestSegmentIntersection(unittest.TestCase):
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

    def test_intersection_reversal(self):
        i = line_intersection(Vector([-10, 10]), Vector([10, -10]),
                              Vector([10, -10]), Vector([-10, 10]))

        self.assertIsNotNone(i)
        self.assertIsInstance(i, Tuple)
        if isinstance(i, Tuple):
            self.assertEqual(2, len(i))

        i = line_intersection(Vector([10, 10]), Vector([-10, -10]),
                              Vector([-10, -10]), Vector([10, 10]))

        self.assertIsNotNone(i)
        self.assertIsInstance(i, Tuple)
        if isinstance(i, Tuple):
            self.assertEqual(2, len(i))


class TestRaySegmentIntersection(unittest.TestCase):
    def test_intersection(self):
        segment = Segment([Vector(5, 0), Vector(5, 10)])
        ray = Line(origin=Vector(0, 5), direction=Vector(1, 0))

        result = ray_segment_intersection(ray, segment)
        self.assertIsNotNone(result)

        if result is not None:
            self.assertAlmostEqual(result.x, 5)
            self.assertAlmostEqual(result.y, 5)

        segment = Segment([Vector(5, 0), Vector(5, 10)])
        ray = Line(origin=Vector(10, 0), direction=Vector(0, 1))

        result = ray_segment_intersection(ray, segment)
        self.assertIsNone(result)

        segment = Segment([Vector(0, 0), Vector(10, 10)])
        ray = Line(origin=Vector(0, 5), direction=Vector(1, 0))

        result = ray_segment_intersection(ray, segment)
        self.assertIsNotNone(result)

        if result is not None:
            self.assertAlmostEqual(result.x, 5)
            self.assertAlmostEqual(result.y, 5)

    def test_offset_intersection(self):
        segment = Segment([Vector(107, 148),
                          Vector(82, 59)])
        ray = Line(origin=Vector(72, 104), direction=Vector(1, 0))

        result = ray_segment_intersection(ray, segment)
        self.assertIsNotNone(result)

        if result is not None:
            self.assertAlmostEqual(result.x, 94.64, 2)
            self.assertAlmostEqual(result.y, 104)
