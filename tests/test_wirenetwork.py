import unittest

from gsnlib.wirenetwork import WireNetwork, Edge
from gsnlib.geometry import Point


class TestWireNetwork(unittest.TestCase):
    def test_non_crossing(self):
        n = WireNetwork()
        n.add_segment([0, 0], [10, 0])
        n.add_segment([0, 2], [10, 2])

        self.assertEqual(len(n.vertices), 4)
        self.assertEqual(len(n.edges), 2)

    def test_cross(self):
        n = WireNetwork()

        n.add_segment([-10, -10], [10, 10])
        n.add_segment([-10, 10], [10, -10])

        self.assertEqual(len(n.vertices), 5)
        self.assertEqual(len(n.edges), 4)

    def test_two_crossing(self):
        n = WireNetwork()

        n.add_segment([2, 2], [2, -2])
        n.add_segment([4, 2], [4, -2])
        n.add_segment([0, 0], [10, 0])

        self.assertEqual(len(n.vertices), 8)
        self.assertEqual(len(n.edges), 7)

        for pair in zip(n.vertices, [Point([2, 2]), Point([2, -2]),
                                     Point([4, 2]), Point([4, -2]),
                                     Point([0, 0]), Point([10, 0]),
                                     Point([2, 0]), Point([4, 0])]):
            self.assertAlmostEqual(pair[0].dist(pair[1]), 0)

        self.assertListEqual(n.edges, [Edge(0, 6), Edge(1, 6),
                                       Edge(2, 7), Edge(3, 7),
                                       Edge(4, 6), Edge(6, 7),
                                       Edge(7, 5)])
