from typing import Dict, List


class lsystem:
    rules: Dict[str, str] = {}
    variables: List[str] = []
    state = None
    axiom = ''

    def __init__(self):
        pass

    def add_variable(self, var: str):
        self.variables.append(var)

    def add_rule(self, rule: str, result: str):
        self.rules[rule] = result

    def add_constant(self, rule: str):
        self.rules[rule] = rule

    def get_state(self):
        if self.state is None:
            return self.axiom

        return self.state

    def update(self, iterations: int = 1):
        for _ in range(iterations):
            state = self.get_state()
            new_state: List[str] = []

            for s_pos in range(len(state)):
                s = state[s_pos]
                new_state.append(self.rules[s])

            self.state = "".join(new_state)
