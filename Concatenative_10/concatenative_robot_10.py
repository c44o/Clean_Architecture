import shlex
import pure_robot

class StackUnderflowError(Exception):
    pass

class UnknownWordError(Exception):
    pass

def pop_value_from_stack(stack, robot_command_name):
    if not stack:
        raise StackUnderflowError(f"не хватает аргументов для команды {robot_command_name}")
    return stack.pop()


def parse_program_atom(token):
    try:
        return int(token)
    except ValueError:
        pass

    try:
        return float(token)
    except ValueError:
        pass

    return token

class RobotServer:
    def __init__(self, transfer=None, initial_state=None):
        if transfer is None:
            transfer = pure_robot.transfer_to_cleaner

        if initial_state is None:
            initial_state = pure_robot.RobotState(
                x=0,
                y=0,
                angle=0,
                state=pure_robot.WATER
            )

        self.transfer = transfer
        self.state = initial_state

        self.words = {
            "move": self.move_robot,
            "turn": self.turn_robot,
            "set": self.set_robot_state,
            "start": self.start_robot,
            "stop": self.stop_robot,
        }

    def move_robot(self, stack):
        distance = pop_value_from_stack(stack, "move")
        self.state = pure_robot.move(self.transfer, distance, self.state)

    def turn_robot(self, stack):
        angle = pop_value_from_stack(stack, "turn")
        self.state = pure_robot.turn(self.transfer, angle, self.state)

    def set_robot_state(self, stack):
        new_mode = pop_value_from_stack(stack, "set")
        self.state = pure_robot.set_state(self.transfer, new_mode, self.state)

    def start_robot(self, stack):
        self.state = pure_robot.start(self.transfer, self.state)

    def stop_robot(self, stack):
        self.state = pure_robot.stop(self.transfer, self.state)

    def execute(self, program):
        stack = []
        tokens = shlex.split(program)

        for token in tokens:
            if token in self.words:
                self.words[token](stack)
            else:
                stack.append(parse_program_atom(token))

        return stack, self.state
