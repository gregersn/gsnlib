import numpy as np
import random
import unittest
from gsnlib.vector import Vector


class TestVector(unittest.TestCase):
    def test_init(self):
        p = Vector(0, 1)
        self.assertEqual(p.x, 0)
        self.assertEqual(p.y, 1)
        self.assertEqual(p.z, 0)

        self.assertTrue(np.array_equal(p.v, np.array([0, 1, 0])))

    def test_repr(self):
        p = Vector(0, 0)
        self.assertEqual(repr(p), "Vector(0, 0, 0)")

        p = Vector(-4, 3)
        self.assertEqual(repr(p), "Vector(-4, 3, 0)")

    def test_properties(self):
        a = random.random()
        b = random.random()

        p = Vector(a, b)

        self.assertAlmostEqual(p.x, a)
        self.assertAlmostEqual(p.y, b)

    def test_lt(self):
        a = Vector(0, 0)
        b = Vector(-1, 0)

        self.assertTrue(b < a)
        self.assertFalse(a < b)

    def test_sub(self):
        a = Vector(0, 0)
        b = Vector(-1, 0)

        c = a - b
        self.assertEqual(c.x, 1)
        self.assertEqual(c.y, 0)

    def test_dist(self):
        a = Vector(0, 0)
        b = Vector(3, 4)
        self.assertEqual(a.dist(b), 5)

    def test_lerp(self):
        v1 = Vector(0, 10)
        v2 = Vector(0, -10)

        v3 = v1.lerp(v2, .5)

        self.assertAlmostEqual(v3.x, 0)
        self.assertAlmostEqual(v3.y, 0)
