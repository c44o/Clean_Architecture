from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import SimpleNamespace
from typing import Callable, NamedTuple, Optional, Any
import math


class CleaningMode(Enum):
    WATER = 1
    SOAP = 2
    BRUSH = 3


class MoveResponse:
    OK = "MOVE_OK"
    NOT_OK = "HIT_BARRIER"


@dataclass(frozen=True)
class RobotView:
    x: float
    y: float
    angle: float
    mode: CleaningMode
    is_cleaning: bool
    blocked: bool
    last_result: Optional[str]


class _InternalState(NamedTuple):
    x: float
    y: float
    angle: float
    mode: CleaningMode
    is_cleaning: bool
    blocked: bool
    last_result: Optional[str]


def transfer_to_cleaner(message: Any) -> None:
    print(message)


def check_position(x: float, y: float) -> tuple[float, float, str]:
    constrained_x = max(0, min(100, x))
    constrained_y = max(0, min(100, y))

    if x == constrained_x and y == constrained_y:
        return constrained_x, constrained_y, MoveResponse.OK

    return constrained_x, constrained_y, MoveResponse.NOT_OK


def create_robot(
    transfer_fn: Callable[[Any], None],
    *,
    has_water: bool = True,
    has_soap: bool = True,
):
    initial_state = _InternalState(
        x=0.0,
        y=0.0,
        angle=0.0,
        mode=CleaningMode.WATER,
        is_cleaning=False,
        blocked=False,
        last_result=None,
    )

    def can_start(state: _InternalState) -> bool:
        if state.mode == CleaningMode.WATER and not has_water:
            return False
        if state.mode == CleaningMode.SOAP and not has_soap:
            return False
        return True

    def make_view(state: _InternalState) -> RobotView:
        return RobotView(
            x=state.x,
            y=state.y,
            angle=state.angle,
            mode=state.mode,
            is_cleaning=state.is_cleaning,
            blocked=state.blocked,
            last_result=state.last_result,
        )

    def build_api(state: _InternalState):
        ops = {}

        def view() -> RobotView:
            return make_view(state)

        def available() -> tuple[str, ...]:
            return tuple(sorted(name for name in ops.keys() if name not in ("view", "available")))

        ops["view"] = view
        ops["available"] = available

        def turn(angle: float):
            new_state = _InternalState(
                x=state.x,
                y=state.y,
                angle=state.angle + angle,
                mode=state.mode,
                is_cleaning=state.is_cleaning,
                blocked=False,
                last_result=f"TURN {angle}",
            )
            transfer_fn(("ANGLE", new_state.angle))
            return build_api(new_state)

        ops["turn"] = turn

        if not state.blocked:
            def move(distance: float):
                angle_rads = state.angle * (math.pi / 180.0)
                raw_x = state.x + distance * math.cos(angle_rads)
                raw_y = state.y + distance * math.sin(angle_rads)

                new_x, new_y, result = check_position(raw_x, raw_y)

                new_state = _InternalState(
                    x=new_x,
                    y=new_y,
                    angle=state.angle,
                    mode=state.mode,
                    is_cleaning=state.is_cleaning,
                    blocked=(result == MoveResponse.NOT_OK),
                    last_result=result,
                )

                if result == MoveResponse.OK:
                    transfer_fn(("POS(", new_state.x, ",", new_state.y, ")"))
                else:
                    transfer_fn(("NOT_OK -> POS(", new_state.x, ",", new_state.y, ")"))

                return build_api(new_state)

            ops["move"] = move

        if not state.is_cleaning:
            if has_water and state.mode != CleaningMode.WATER:
                def use_water():
                    new_state = _InternalState(
                        x=state.x,
                        y=state.y,
                        angle=state.angle,
                        mode=CleaningMode.WATER,
                        is_cleaning=False,
                        blocked=state.blocked,
                        last_result="STATE_OK",
                    )
                    transfer_fn(("STATE", CleaningMode.WATER.value))
                    return build_api(new_state)

                ops["use_water"] = use_water

            if has_soap and state.mode != CleaningMode.SOAP:
                def use_soap():
                    new_state = _InternalState(
                        x=state.x,
                        y=state.y,
                        angle=state.angle,
                        mode=CleaningMode.SOAP,
                        is_cleaning=False,
                        blocked=state.blocked,
                        last_result="STATE_OK",
                    )
                    transfer_fn(("STATE", CleaningMode.SOAP.value))
                    return build_api(new_state)

                ops["use_soap"] = use_soap

            if state.mode != CleaningMode.BRUSH:
                def use_brush():
                    new_state = _InternalState(
                        x=state.x,
                        y=state.y,
                        angle=state.angle,
                        mode=CleaningMode.BRUSH,
                        is_cleaning=False,
                        blocked=state.blocked,
                        last_result="STATE_OK",
                    )
                    transfer_fn(("STATE", CleaningMode.BRUSH.value))
                    return build_api(new_state)

                ops["use_brush"] = use_brush

        if not state.is_cleaning and can_start(state):
            def start():
                new_state = _InternalState(
                    x=state.x,
                    y=state.y,
                    angle=state.angle,
                    mode=state.mode,
                    is_cleaning=True,
                    blocked=state.blocked,
                    last_result="START_OK",
                )
                transfer_fn(("START WITH", state.mode.value))
                return build_api(new_state)

            ops["start"] = start

        if state.is_cleaning:
            def stop():
                new_state = _InternalState(
                    x=state.x,
                    y=state.y,
                    angle=state.angle,
                    mode=state.mode,
                    is_cleaning=False,
                    blocked=state.blocked,
                    last_result="STOP_OK",
                )
                transfer_fn(("STOP",))
                return build_api(new_state)

            ops["stop"] = stop

        return SimpleNamespace(**ops)

    return build_api(initial_state)


if __name__ == "__main__":
    robot = create_robot(
        transfer_to_cleaner,
        has_water=False,
        has_soap=True,
    )

    print("initial:", robot.view())
    print("available:", robot.available())
    print()

    robot = robot.use_soap()
    print("after use_soap:", robot.view())
    print("available:", robot.available())
    print()

    robot = robot.start()
    robot = robot.move(100)
    robot = robot.turn(-90)
    robot = robot.move(50)

    print("after barrier:", robot.view())
    print("available:", robot.available())
    print()

    robot = robot.turn(90)
    print("after turn:", robot.view())
    print("available:", robot.available())
    print()

    robot = robot.stop()
    print("final:", robot.view())
    print("available:", robot.available())
