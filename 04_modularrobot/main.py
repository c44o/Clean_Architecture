from __future__ import annotations

from domain import Robot
from interpreter import Interpreter


def main() -> None:
    test_program = ["move 100", "turn -90", "set soap", "start", "move 50", "stop"]
    robot = Robot()
    interpreter = Interpreter(robot)
    interpreter.run(test_program)


if __name__ == "__main__":
    main()
