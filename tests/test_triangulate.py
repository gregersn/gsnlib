from gsnlib.geometry.triangulate import triangulate
import unittest

from gsnlib.geometry import Polygon, Vector


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
