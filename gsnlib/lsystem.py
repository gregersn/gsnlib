from typing import Dict


class LSystem(object):
    state: str

    def __init__(self, axiom: str):
        self.axiom = axiom
        self.state = axiom
        self.rules: Dict[str, str] = {}

    def reset(self):
        self.state = self.axiom

    def iterate(self):
        self.state = "".join([self.rules.get(c, c) for c in self.state])
        return self.state

    def add_rule(self, case: str, result: str):
        self.rules[case] = result
