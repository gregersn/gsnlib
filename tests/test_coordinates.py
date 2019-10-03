import unittest
import math
import sys
from gsnlib.coordinates import Coordinates


epsilon = sys.float_info.epsilon * 10


class TestIdentity(unittest.TestCase):
    def test_init(self):
        c = Coordinates()
        pos = c.pos
        self.assertEqual(pos[0], 0)
        self.assertEqual(pos[1], 0)
    
    def test_reset(self):
        c = Coordinates()
        pos = c.pos
        self.assertEqual(pos[0], 0)
        self.assertEqual(pos[1], 0)

        c.translate(1, 2)
        pos = c.pos
        self.assertNotEqual(pos[0], 0)
        self.assertNotEqual(pos[1], 0)

        c.reset()
        pos = c.pos
        self.assertEqual(pos[0], 0)
        self.assertEqual(pos[1], 0)


class TestTranslation(unittest.TestCase):
    def test_translate(self):
        c = Coordinates()
        for i in range(1, 10):
            c.translate(10, 5)
            pos = c.pos

            self.assertEqual(pos[0], i * 10)
            self.assertEqual(pos[1], i * 5)

    def test_translate_multiple(self):
        c = Coordinates()
        c.translate(10, 5)

        c.translate(2, 10)
        pos = c.pos

        self.assertEqual(pos[0], 12)
        self.assertEqual(pos[1], 15)


class TestScale(unittest.TestCase):
    def test_scale_up(self):
        c = Coordinates()
        c.scale(2)
        c.translate(2, 3)
        pos = c.pos
        self.assertEqual(pos[0], 4)
        self.assertEqual(pos[1], 6)

    def test_scale_down(self):
        c = Coordinates()
        c.scale(.5)
        c.translate(2, 3)
        pos = c.pos
        self.assertEqual(pos[0], 1)
        self.assertEqual(pos[1], 1.5)


class TestRotate(unittest.TestCase):
    def test_rotate_ccw(self):
        c = Coordinates()
        c.rotate(math.pi / 2)
        c.translate(1, 0)

        pos = c.pos
        self.assertAlmostEqual(pos[0], epsilon)
        self.assertAlmostEqual(pos[1], 1)

    def test_rotate_cw(self):
        c = Coordinates()
        c.rotate(-math.pi / 2)
        c.translate(1, 0)

        pos = c.pos
        self.assertAlmostEqual(pos[0], epsilon)
        self.assertAlmostEqual(pos[1], -1)

    def test_rotate_multiple(self):
        c = Coordinates()
        c.translate(1, 0)
        for i in range(8):
            c.rotate(math.pi / 4)

        self.assertLess(abs(c.pos[0] - 1), epsilon)
        self.assertLess(c.pos[1], epsilon)
    
    def test_rotate_translate(self):
        c = Coordinates()

        c.translate(0, 10)
        self.assertEqual(c.x, 0)
        self.assertEqual(c.y, 10)

        c.reset()
        c.rotate(math.pi / 2)
        c.translate(0, 10)
        self.assertEqual(c.x, -10)
        self.assertEqual(c.y, 0)



class TestTranslateRotateSequence(unittest.TestCase):
    def test_back_and_forth(self):
        c = Coordinates()
        c.translate(10, 0)
        c.translate(-10, 0)

        self.assertLess(c.pos[0], epsilon)
        self.assertLess(c.pos[1], epsilon)

    def test_there_and_back(self):
        c = Coordinates()
        c.translate(10, 0)
        c.rotate(math.pi)
        c.translate(10, 0)

        self.assertLess(c.pos[0], epsilon)
        self.assertLess(c.pos[1], epsilon)

    def test_square(self):
        c = Coordinates()
        c.translate(10, 0)
        c.rotate(math.pi / 2)
        c.translate(10, 0)
        c.rotate(math.pi / 2)
        c.translate(10, 0)
        c.rotate(math.pi / 2)
        c.translate(10, 0)

        self.assertLess(c.pos[0], epsilon)
        self.assertLess(c.pos[1], epsilon)

    def test_wander(self):
        c = Coordinates()

        for i in range(1, 10):
            c.translate(10, 0)
            
            self.assertAlmostEqual(c.x, 10 * i)
            self.assertAlmostEqual(c.y, 10 * (i - 1))

            c.rotate(math.pi / 2)
            c.translate(10, 0)
            
            self.assertAlmostEqual(c.x, 10 * i)
            self.assertAlmostEqual(c.y, 10 * i)
            
            c.rotate(-math.pi / 2)


class TestStack(unittest.TestCase):
    def test_push_pop(self):
        c = Coordinates()
        c.translate(1, 0)

        c.push()

        self.assertEqual(c.pos[0], 1)
        self.assertEqual(c.pos[1], 0)

        c.translate(1, 0)

        c.pop()

        self.assertEqual(c.pos[0], 1)
        self.assertEqual(c.pos[1], 0)
