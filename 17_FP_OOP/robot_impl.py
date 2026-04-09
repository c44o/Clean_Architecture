from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import math


class CleaningMode(Enum):
    WATER = 1
    SOAP = 2
    BRUSH = 3


@dataclass(frozen=True)
class MoveResult:
    robot: "Robot"
    moved_distance: float
    success: bool


@dataclass(frozen=True)
class SetModeResult:
    robot: "Robot"
    mode: CleaningMode
    success: bool


class Robot:
    @dataclass(frozen=True)
    class _State:
        x: float
        y: float
        angle: float
        mode: CleaningMode

    __slots__ = ("_state",)

    def __init__(self, state: "Robot._State"):
        self._state = state

    @classmethod
    def create(cls) -> "Robot":
        return cls(
            cls._State(
                x=0.0,
                y=0.0,
                angle=0.0,
                mode=CleaningMode.WATER,
            )
        )


    @property
    def x(self) -> float:
        return self._state.x

    @property
    def y(self) -> float:
        return self._state.y

    @property
    def angle(self) -> float:
        return self._state.angle

    @property
    def mode(self) -> CleaningMode:
        return self._state.mode

    def position(self) -> tuple[float, float]:
        return (self._state.x, self._state.y)

    # идея - всегда возврашать новый Robot
    def move(self, distance: float) -> MoveResult:
        angle_rads = self._state.angle * (math.pi / 180.0)

        new_x = self._state.x + distance * math.cos(angle_rads)
        new_y = self._state.y + distance * math.sin(angle_rads)

        new_robot = Robot(
            Robot._State(
                x=new_x,
                y=new_y,
                angle=self._state.angle,
                mode=self._state.mode,
            )
        )

        return MoveResult(
            robot=new_robot,
            moved_distance=distance,
            success=True,
        )

    def turn(self, angle: float) -> "Robot":
        return Robot(
            Robot._State(
                x=self._state.x,
                y=self._state.y,
                angle=self._state.angle + angle,
                mode=self._state.mode,
            )
        )

    def set_mode(self, new_mode: CleaningMode) -> SetModeResult:
        new_robot = Robot(
            Robot._State(
                x=self._state.x,
                y=self._state.y,
                angle=self._state.angle,
                mode=new_mode,
            )
        )

        return SetModeResult(
            robot=new_robot,
            mode=new_mode,
            success=True,
        )

    def start(self) -> "Robot":
        return self

    def stop(self) -> "Robot":
        return self

    def __repr__(self) -> str:
        return (
            f"Robot(x={self._state.x:.2f}, "
            f"y={self._state.y:.2f}, "
            f"angle={self._state.angle:.2f}, "
            f"mode={self._state.mode.name})"
        )
