import unittest

from gsnlib.graph import Graph


class TestGraph(unittest.TestCase):
    def test_simple(self):
        g = Graph()
        self.assertTrue(g.simple)

        g.add_edge(0, 1)
        self.assertTrue(g.simple)

    def test_loops(self):
        g = Graph()
        self.assertFalse(g.loops)

        g.add_edge(0, 1)
        self.assertFalse(g.loops)

        g.add_edge(1, 1)
        self.assertTrue(g.loops)

    def test_multiples(self):
        g = Graph()
        self.assertFalse(g.multiples)

        g.add_edge(0, 1)
        self.assertFalse(g.multiples)

        g.add_edge(0, 1)
        self.assertTrue(g.multiples)
