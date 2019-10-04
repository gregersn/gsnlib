import unittest

from gsnlib.lsystem import LSystem


class TestLSystem(unittest.TestCase):
    def test_add_rules(self):
        s = LSystem('a')
        s.add_rule('a', 'b')
        s.add_rule('b', 'aa')

        self.assertEqual(len(s.rules), 2)

    def test_iterate(self):
        s = LSystem('a')
        s.add_rule('a', 'b')
        s.add_rule('b', 'aa')

        res = s.iterate()
        self.assertEqual(res, 'b')

        res = s.iterate()
        self.assertEqual(res, 'aa')

        res = s.iterate()
        self.assertEqual(res, 'bb')

        s.reset()
        self.assertEqual(s.state, 'a')
