class LSystem(object):
    def __init__(self, axiom: str):
        self.axiom = axiom
        self.state = axiom
        self.rules = {}

    def reset(self):
        self.state = self.axiom

    def iterate(self):
        self.state = "".join([self.rules.get(c, c) for c in self.state])
        return self.state

    def add_rule(self, case, result):
        self.rules[case] = result
