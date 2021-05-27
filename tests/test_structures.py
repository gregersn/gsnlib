import unittest
from gsnlib.structures.circularsorted import CircularSorted


class TestCircularSorted(unittest.TestCase):
    def test_init(self):
        cs = CircularSorted()

        cs.append(1)

        self.assertEqual(len(cs), 1)

        cs.append(2)
        self.assertEqual(len(cs), 2)

    def test_add_stuff(self):
        cs = CircularSorted()

        cs.append(2)
        self.assertEqual(cs.data, [2], cs.data)

        cs.append(5)
        self.assertEqual(cs.data, [2, 5], cs.data)

        cs.append(1)
        self.assertEqual(cs.data, [2, 5, 1], cs.data)

        cs.append(3)
        self.assertEqual(cs.data, [2, 3, 5, 1], cs.data)

        cs.pop(0)
        self.assertEqual(cs.data, [3, 5, 1], cs.data)
