from collections import namedtuple
import math

RobotState = namedtuple("RobotState", "x y angle state")

WATER = 1
SOAP = 2
BRUSH = 3


class MoveResponse:
    OK = "MOVE_OK"
    BARRIER = "HIT_BARRIER"


class SetStateResponse:
    OK = "STATE_OK"
    NO_WATER = "OUT_OF_WATER"
    NO_SOAP = "OUT_OF_SOAP"


class StateMonad:
    def __init__(self, state, log=None, responses=None):
        self.state = state
        self.log = log or []
        self.responses = responses or []

    def bind(self, func):
        new_state, new_log, response = func(self.state, self.log)

        new_responses = self.responses[:]
        if response is not None:
            new_responses.append(response)

        return StateMonad(new_state, new_log, new_responses)


def check_position(x: float, y: float) -> tuple[float, float, str]:
    constrained_x = max(0, min(100, x))
    constrained_y = max(0, min(100, y))

    if x == constrained_x and y == constrained_y:
        return (x, y, MoveResponse.OK)

    return (constrained_x, constrained_y, MoveResponse.BARRIER)


HAS_WATER = False
HAS_SOAP = True


def check_resources(new_mode: int) -> str:
    if new_mode == WATER and not HAS_WATER:
        return SetStateResponse.NO_WATER

    if new_mode == SOAP and not HAS_SOAP:
        return SetStateResponse.NO_SOAP

    return SetStateResponse.OK


def move(dist):
    def inner(old_state, log):
        angle_rads = old_state.angle * (math.pi / 180.0)

        raw_x = old_state.x + dist * math.cos(angle_rads)
        raw_y = old_state.y + dist * math.sin(angle_rads)

        checked_x, checked_y, response = check_position(raw_x, raw_y)

        new_state = RobotState(
            checked_x,
            checked_y,
            old_state.angle,
            old_state.state
        )

        if response == MoveResponse.OK:
            new_log = log + [f"POS({int(new_state.x)},{int(new_state.y)})"]
        else:
            new_log = log + [f"HIT_BARRIER -> POS({int(new_state.x)},{int(new_state.y)})"]

        return new_state, new_log, response

    return inner


def turn(angle):
    def inner(old_state, log):
        new_state = RobotState(
            old_state.x,
            old_state.y,
            old_state.angle + angle,
            old_state.state
        )
        return new_state, log + [f"ANGLE {new_state.angle}"], None

    return inner


def set_state(new_mode):
    def inner(old_state, log):
        response = check_resources(new_mode)

        if response != SetStateResponse.OK:
            return old_state, log + [response], response

        new_state = RobotState(
            old_state.x,
            old_state.y,
            old_state.angle,
            new_mode
        )
        return new_state, log + [f"STATE {new_mode}"], response

    return inner


def start(old_state, log):
    return old_state, log + ["START"], None


def stop(old_state, log):
    return old_state, log + ["STOP"], None


initial_state = StateMonad(RobotState(0.0, 0.0, 0, WATER))

result = (
    initial_state
    .bind(move(100))
    .bind(turn(-90))
    .bind(set_state(SOAP))
    .bind(start)
    .bind(move(50))
    .bind(stop)
)

print("Final state:", result.state)
print("Log:", result.log)
print("Responses:", result.responses)
