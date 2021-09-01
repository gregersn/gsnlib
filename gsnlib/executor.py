from typing import Callable, Dict


class Executor(object):
    def __init__(self):
        self.instructions: Dict[str, Callable[..., None]] = {}
        self.reset()

    def reset(self):
        self.ip = 0
        self.program = ""

    def add_instruction(self, command: str, function: Callable[..., None]):
        self.instructions[command] = function

    def step(self):
        command = self.program[self.ip]
        self.instructions[command]()
        self.ip += 1
