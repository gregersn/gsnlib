import math
from gsnlib.geometry.triangulate import triangulate, calc_next, calc_prev
from gsnlib.geometry.triangulate import check_ear, tri_angle
import unittest
from typing import List

from gsnlib.geometry import Polygon, Vector

TEST_POINTS = [
    Vector(9.321044, 84.581885),
    Vector(61.315102, 127.09138),
    Vector(111.49942, 82.482205),
    Vector(152.6412, 109.31529),
    Vector(192.03188, 53.63302),
    Vector(145.06825, 59.025564),
    Vector(124.16278, 15.675397),
    Vector(82.50756, 90.121654),
    Vector(33.765241, 77.262587),
    Vector(37.242697, 29.545994)
]


class TestHelpers(unittest.TestCase):
    def test_calc_next(self):
        self.assertEqual(calc_next(0, 3), 1)
        self.assertEqual(calc_next(1, 3), 2)
        self.assertEqual(calc_next(2, 3), 0)

    def test_calc_prev(self):
        self.assertEqual(calc_prev(0, 3), 2)
        self.assertEqual(calc_prev(1, 3), 0)
        self.assertEqual(calc_prev(2, 3), 1)

    def test_tri_angle(self):
        self.assertGreater(math.pi, tri_angle(
            TEST_POINTS[4], TEST_POINTS[5], TEST_POINTS[2]))

        self.assertLess(math.pi, tri_angle(
            TEST_POINTS[2], TEST_POINTS[4], TEST_POINTS[1]
        ))

    def test_check_ear(self):
        self.assertFalse(
            check_ear(Polygon([TEST_POINTS[0], TEST_POINTS[1], TEST_POINTS[9]]), [
                      TEST_POINTS[8]]))

        self.assertTrue(
            check_ear(Polygon([TEST_POINTS[0], TEST_POINTS[1], TEST_POINTS[9]]), [
                      TEST_POINTS[7]]))


class TestConvex(unittest.TestCase):
    def test_triangle(self):
        tri = Polygon(
            [Vector(0, 0), Vector(0, 10), Vector(10, 10)]
        )

        output = triangulate(tri)
        self.assertEqual(len(output), 1)
        self.assertEqual(tri, output[0])

    def test_quad(self):
        quad = Polygon(
            [Vector(0, 0), Vector(0, 10), Vector(10, 10), Vector(10, 0)])

        output = triangulate(quad)

        self.assertEqual(len(output), 2)

        self.assertEqual(output[0].points, [Vector(
            10, 0), Vector(0, 0), Vector(0, 10)])

        self.assertEqual(output[1].points, [Vector(
            0, 10), Vector(10, 10), Vector(10, 0)])

    def test_misc(self):

        TEST_CASES = [
            {
                'poly': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                'results': [
                    [2, 3, 4],
                    [2, 4, 5],
                    [2, 5, 6],
                    [2, 6, 7],
                    [8, 9, 0],
                    [8, 0, 1],
                    [1, 2, 7],
                    [1, 7, 8]
                ]
            }

        ]

        for case in TEST_CASES:
            poly_indices: List[int] = case['poly']
            result_polys = case['results']

            poly = Polygon([TEST_POINTS[i] for i in poly_indices])

            output = triangulate(poly)

            for idx, p in enumerate(output):
                result_points = [TEST_POINTS[i] for i in result_polys[idx]]

                self.assertEqual(result_points, p.points,
                                 f'Comparing poly {idx}: {result_polys[idx]}, and got {[TEST_POINTS.index(pp) for pp in p.points]}')

    def test_convex(self):
        poly = Polygon(
            [Vector(0, 0), Vector(10, 0), Vector(10, 10),
             Vector(5, 2), Vector(0, 10)]
        )
        output = triangulate(poly)

        self.assertEqual(len(output), 3)

        self.assertEqual(output[0].points, [
                         poly.points[2], poly.points[3], poly.points[1]])

        self.assertEqual(output[1].points, [
                         poly.points[1], poly.points[3], poly.points[0]])

        self.assertEqual(output[2].points, [
                         poly.points[0], poly.points[3], poly.points[4]])

    def test_complex(self):
        """
        poly = Polygon(
            [Vector(0.62731574, 118.02858),
             Vector(89.605676, 191.80027),
             Vector(174.11161, 115.47713),
             Vector(243.90512, 160.90282),
             Vector(312.51194, 66.529942),
             Vector(231.77231, 76.642446),
             Vector(197.08373, 1.096719),
             Vector(125, 128.80745),
             Vector(42.161777, 107.42186),
             Vector(48.132897, 24.908423)]
        )
        """

        poly = Polygon(
            [Vector(0.18961914, 0.06754579),
             Vector(19.043604, 15.154766),
             Vector(37.208456, -0.8185475),
             Vector(51.906456, 9.3371793),
             Vector(66.111665, -11.042135),
             Vector(49.119031, -8.846688),
             Vector(41.649933, -25.039257),
             Vector(26.747961, 2.7334792),
             Vector(9.032703, -2.6351076),
             Vector(10.552048, -20.037214)])

        output = triangulate(poly)

        """
        Round 1:
            convex = [0, 1, 3, 4, 6, 9]
            reflex = [2, 5, 7, 8]
            ear = [3, 4, 6, 9]
            triangle = <2, 3, 4>

        Round 2:
            ear = [4, 6, 9]
            triangle = <2, 4, 5>

        Round 3:
            ears = [5, 6, 9]
            reflex = [2, 7, 8]
            convex = [0, 1, 6, 9, 5]
            triangle = <2, 5, 6>

        Round 4:
            reflex = [7, 8]
            convex = [0, 1, 2, 6, 9]
            ears = [6, 9]
            triangle = <2, 6, 7>

        Round 5:
            reflex = [7, 8]
            ears = [9, 2]
            triangle = <8, 9, 0>
        """

        self.assertEqual(len(output), 8)
