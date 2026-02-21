from dataclasses import dataclass
from typing import Optional 
import math

@dataclass
class Command:
    name: str
    arg: Optional[float] = None


class Robot:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.angle = 0.0
        self.mode = "water"
        self.is_cleaning = False


    def move(self, distance: float): 
        # move code
        radians = math.radians(self.angle)
        self.x += distance * math.cos(radians)
        self.y += distance * math.sin(radians)

        print(f"POS {self.x:.2f}, {self.y:.2f}")


    def turn(self, rotation_angle: float):
        self.angle = (self.angle + rotation_angle) % 360.0

        print(f"ANGLE {self.angle:.2f}")

    
    def set(self, mode: str):
        self.mode = mode 
        # считаем, что можно менять режим на лету
        print(f"STATE {self.mode}")


    def start(self, _=None):
        self.is_cleaning = True

        print(f"START WITH {self.mode}")
    

    def stop(self, _=None):
        self.is_cleaning = False
        print(f"STOP")


class Interpreter:
    def __init__(self, robot: Robot):
        self.robot = robot
        self.available_commands = {
        "move": robot.move, 
        "turn": robot.turn,
        "set": robot.set,
        "start": robot.start, 
        "stop": robot.stop
    }

    def parse_command(self, line: str) -> Command:
        line = line.strip()
        if not line:
            raise ValueError("comand is empty")
        line_halves = line.split()
        command_name = line_halves[0].lower()

        if command_name not in ("move", "turn", "set", "start", "stop"):
            raise ValueError("command is unfamiliar")
        
        if command_name in ("start", "stop"):
            if len(line_halves) != 1:
                raise ValueError("command have no arguments")
            return Command(name=command_name, arg=None)
        
        if len(line_halves) != 2:
            raise ValueError("there is only one argument")
        
        if command_name in ('move', 'turn'): 
            try:
                command_arg = float(line_halves[1])
            except:
                raise ValueError(f"{line_halves[1]} is not compatible with move or turn commands")
            return Command(name=command_name, arg=command_arg)

        if command_name == "set":
            mode = line_halves[1].lower()
            if line_halves[1] not in ("water", "soap", "brush"):
                raise ValueError(f"{line_halves[1]} not applicable for mode command")
            return Command(name=command_name, arg=mode)
    
    def run(self, command_strings: list[str]):
        for command_string in command_strings:
            cmd = self.parse_command(command_string)
            self.available_commands[cmd.name](cmd.arg)

if __name__ == "__main__":
    test_program = ["move 100", "turn -90", "set soap", "start", "move 50", "stop"]
    test_robot = Robot()
    interpreter = Interpreter(test_robot)
    interpreter.run(test_program)
