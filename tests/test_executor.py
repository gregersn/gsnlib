import unittest
from gsnlib.executor import Executor


class TestExectuor(unittest.TestCase):
    def test_step(self):
        class T(object):
            def __init__(self):
                self.foo = 0

            def incfoo(self):
                self.foo += 1

        t = T()
        e = Executor()
        self.assertEqual(t.foo, 0)
        e.add_instruction('a', t.incfoo)
        e.program = 'a'
        e.step()

        self.assertEqual(t.foo, 1)
