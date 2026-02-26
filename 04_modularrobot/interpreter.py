from __future__ import annotations

from domain import Robot
from parser import parse_command


class Interpreter:
    def __init__(self, robot: Robot):
        self.robot = robot

    def run(self, program_lines: list[str]) -> None:
        for line in program_lines:
            cmd = parse_command(line)
            cmd.execute(self.robot)
