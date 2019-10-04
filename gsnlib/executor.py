class Executor(object):
    def __init__(self):
        self.instructions = {}
        self.reset()

    def reset(self):
        self.ip = 0
        self.program = ""

    def add_instruction(self, command: str, function):
        self.instructions[command] = function

    def step(self):
        command = self.program[self.ip]
        self.instructions[command]()
        self.ip += 1
