#!/usr/bin/python
# -*- coding: utf8 -*-


class lsystem(object):
    rules = {}
    variables = []
    state = None
    axiom = ''

    def __init__(self):
        pass

    def add_variable(self, var):
        self.variables.append(var)

    def add_rule(self, rule, result):
        self.rules[rule] = result

    def add_constant(self, rule):
        self.rules[rule] = rule

    def get_state(self):
        if self.state is None:
            return self.axiom

        return self.state

    def update(self, iterations=1):
        for i in range(iterations):
            state = self.get_state()
            new_state = []

            for s_pos in range(len(state)):
                s = state[s_pos]
                new_state.append(self.rules[s])

            self.state = "".join(new_state)
