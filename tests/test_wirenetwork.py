import unittest
import random

from gsnlib.wirenetwork import WireNetwork, Edge
from gsnlib.vector import Vector


class TestWireNetworkLoadSave(unittest.TestCase):
    def test_to_from_to(self):
        n = WireNetwork()
        n.add_segment([0, 0], [10, 10])

        data = n.to_dict()

        self.assertIsNotNone(data)
        self.assertIn('vertices', data)
        self.assertIn('edges', data)

        self.assertEqual(len(data['vertices']), 2)
        self.assertEqual(len(data['edges']), 1)

        o = WireNetwork()
        o.from_dict(data)

        self.assertEqual(data, o.to_dict())
        self.assertEqual(len(o._vertices), 2)
        self.assertEqual(len(o._edges), 1)

    def test_from_to_random(self):
        n = WireNetwork()

        for _ in range(10):
            n.add_segment([random.randrange(-100, 100),
                           random.randrange(-100, 100)],
                          [random.randrange(-100, 100),
                           random.randrange(-100, 100)])

        data = n.to_dict()

        o = WireNetwork()
        o.from_dict(data)

        self.assertDictEqual(data, o.to_dict())


class TestWireNetwork(unittest.TestCase):
    def test_non_crossing(self):
        n = WireNetwork()
        n.add_segment([0, 0], [10, 0])
        n.add_segment([0, 2], [10, 2])

        self.assertEqual(len(n.vertices), 4, msg=n.vertices)
        self.assertEqual(len(n.edges), 2, msg=n.edges)

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

        for pair in zip(sorted(n.vertices), sorted([Vector([2, -2]),
                                                    Vector([2, 2]),
                                                    Vector([4, -2]),
                                                    Vector([4, 2]),
                                                    Vector([0, 0]),
                                                    Vector([10, 0]),
                                                    Vector([2, 0]),
                                                    Vector([4, 0])])):
            self.assertAlmostEqual(pair[0].dist(pair[1]), 0, msg=n.vertices)

        self.assertListEqual(n.edges, [Edge(0, 6), Edge(1, 6),
                                       Edge(2, 7), Edge(3, 7),
                                       Edge(4, 6), Edge(6, 7),
                                       Edge(7, 5)])

    def test_end_to_end(self):
        n = WireNetwork()
        n.add_segment([0, 0], [10, 10])

        self.assertEqual(len(n.vertices), 2)
        self.assertEqual(len(n.edges), 1)

        n.add_segment([10, 10], [20, 20])

        self.assertEqual(len(n.vertices), 3)
        self.assertEqual(len(n.edges), 2, n.edges)

    def test_overlapping(self):
        n = WireNetwork()
        n.add_segment([0, 0], [10, 10])
        n.add_segment([5, 5], [15, 15])

        self.assertEqual(len(n.vertices), 4, n.vertices)
        self.assertEqual(len(n.edges), 3, n.edges)

    def test_within(self):
        n = WireNetwork()
        n.add_segment([4, 4], [8, 8])
        n.add_segment([0, 0], [10, 10])

        self.assertEqual(len(n.vertices), 4, n.vertices)
        self.assertEqual(len(n.edges), 3, n.edges)

        n = WireNetwork()
        n.add_segment([0, 0], [10, 10])
        n.add_segment([4, 4], [8, 8])

        self.assertEqual(len(n.vertices), 2, n.vertices)
        self.assertEqual(len(n.edges), 1, n.edges)

    def test_add_existing(self):
        n = WireNetwork()
        n.add_segment([4, 4], [8, 8])
        n.add_segment([4, 4], [8, 8])

        self.assertEqual(len(n.vertices), 2, n.vertices)
        self.assertEqual(len(n.edges), 1, n.edges)

    def test_add_small_segment(self):
        n = WireNetwork()
        n.add_segment([4, 4], [8, 8])
        n.add_segment([4, 4], [4.0001, 4])

        self.assertEqual(len(n.vertices), 2, n.vertices)
        self.assertEqual(len(n.edges), 1, n.edges)
