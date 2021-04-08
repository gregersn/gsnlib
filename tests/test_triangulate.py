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
            0, 0), Vector(0, 10), Vector(10, 0)])

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
