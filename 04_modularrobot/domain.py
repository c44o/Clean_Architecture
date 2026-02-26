from __future__ import annotations

import math
from enum import Enum
from typing import Callable

class CleaningMode(str, Enum):
    WATER = "water"
    SOAP = "soap"
    BRUSH = "brush"

class Robot:
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
        self.emit(f"POS {self.x:.2f}, {self.y:.2f}")

    def turn(self, rotation_angle:float):
        self.angle = (self.angle + rotation_angle) % 360
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
