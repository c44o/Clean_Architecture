from enum import Enum

# поскольку базовое ООП-решение уже реализовано в первом задании, 
# здесь пробую дальше оформлять логику при помощи именования + разводить данные и обработку с помощью классов
 
# отдельная структура для режимов работы
class CleaningMode(str, Enum):
    WATER = "water"
    SOAP = "soap"
    BRUSH = "brush"

import math
from typing import Callable

class Robot:
    # здесь ещё более явно упаковываем обработку разных видов команд с разным набором аргументов с помощью Callable
    def __init__(self, emit: Callable[[str], None] = print):
        self.x = 0.0
        self.y = 0.0
        self.angle = 0.0
        self.mode = CleaningMode.WATER
        self.is_cleaning = False
        self.emit = emit

    def move(self, distance: float):
        rad = math.radians(self.angle)
        self.x += distance * math.cos(rad)
        self.y += distance * math.sin(rad)

        # в этой и последующих функциях оставляем интерфейс под возможное изменение вывода - не просто print, а print внутри отдельной команды
        self.emit(f"POS {self.x:.2f}, {self.y:.2f}")

    def turn(self, rotation_angle: float):
        self.angle = (self.angle + rotation_angle) % 360.0
        self.emit(f"ANGLE {self.angle:.2f}")

    def set_mode(self, mode: CleaningMode):
        self.mode = mode
        self.emit(f"STATE {self.mode.value}")

    def start(self):
        self.is_cleaning = True
        self.emit(f"START WITH {self.mode.value}")

    def stop(self):
        self.is_cleaning = False
        self.emit("STOP")


# пробую добавить паттерн Command , как его понял
# делаем команды отдельным слоем, все пять - единообразны

from dataclasses import dataclass
from abc import ABC, abstractmethod

# явно обозначить контракт для всех команд
class Command(ABC):
    @abstractmethod
    def execute(self, robot: Robot) -> None: ...

@dataclass(frozen=True)
class Move(Command):
    distance: float
    def execute(self, robot: Robot) -> None:
        robot.move(self.distance)

@dataclass(frozen=True)
class Turn(Command):
    rotation_angle: float
    def execute(self, robot: Robot) -> None:
        robot.turn(self.rotation_angle)

@dataclass(frozen=True)
class Set(Command):
    mode: CleaningMode
    def execute(self, robot: Robot) -> None:
        robot.set_mode(self.mode)

@dataclass(frozen=True)
class Start(Command):
    def execute(self, robot: Robot) -> None:
        robot.start()

@dataclass(frozen=True)
class Stop(Command):
    def execute(self, robot: Robot) -> None:
        robot.stop()

# пытаемся далее аналитически разложить сопоставление ввода с внутренним представлением робота на отдельные элементы
# вместо одной parse_command теперь:
# lex (для превращения строки в токены)

from dataclasses import dataclass

def lex(line: str) -> list[str]:
    line = line.strip()
    if not line:
        raise ValueError("command is empty")
    return line.split()

# parse_syntax c отдельным датаклассом (для разбора команд на одно- и двухаргументные)
@dataclass(frozen=True)
class Parsed:
    name: str
    arg: str | None

def parse_syntax(tokens: list[str]) -> Parsed:
    name = tokens[0].lower()

    if name in ("start", "stop"):
        if len(tokens) != 1:
            raise ValueError(f"'{name}' takes no arguments")
        return Parsed(name=name, arg=None)

    if len(tokens) != 2:
        raise ValueError(f"'{name}' expects exactly 1 argument")
    return Parsed(name=name, arg=tokens[1])

# parse_semantics - для итогового спосоставления ввода с внутренним представлением программы
def parse_semantics(p: Parsed) -> Command:
    if p.name == "start":
        return Start()
    if p.name == "stop":
        return Stop()

    assert p.arg is not None 

    if p.name == "move":
        return Move(float(p.arg))
    if p.name == "turn":
        return Turn(float(p.arg))
    if p.name == "set":
        mode = p.arg.lower()
        return Set(CleaningMode(mode))

    raise ValueError(f"command is unfamiliar {p.name}")

# и parse_command теперь собирает вместе работу этих трёх команд
def parse_command(line: str) -> Command:
    tokens = lex(line)
    parsed = parse_syntax(tokens)
    return parse_semantics(parsed)

# Interpreter теперь нужен только в качестве обёртки над run - то есть это финальная точка, где мы из ввода и внутреннего представления получаем некоторое действие
class Interpreter:
    def __init__(self, robot: Robot):
        self.robot = robot

    def run(self, program_lines: list[str]) -> None:
        for line in program_lines:
            cmd = parse_command(line)
            cmd.execute(self.robot)


if __name__ == "__main__":
    test_program = ["move 100", "turn -90", "set soap", "start", "move 50", "stop"]
    test_robot = Robot()
    interpreter = Interpreter(test_robot)
    interpreter.run(test_program)
