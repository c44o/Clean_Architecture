from dataclasses import dataclass
from typing import List, Union
import pure_robot

# что нужно сделать

@dataclass
class MoveCommand:
    robot_id: str
    distance: float

@dataclass
class TurnCommand:
    robot_id: str
    angle: float

@dataclass
class SetModeCommand:
    robot_id: str
    mode: str

@dataclass
class StartCleaningCommand:
    robot_id: str

@dataclass
class StopCleaningCommand:
    robot_id: str

Command = Union[
    MoveCommand,
    TurnCommand,
    SetModeCommand,
    StartCleaningCommand,
    StopCleaningCommand
]

# что уже сделано

@dataclass
class MovedEvent:
    robot_id: str
    distance: float


@dataclass
class TurnedEvent:
    robot_id: str
    angle: float


@dataclass
class ModeSetEvent:
    robot_id: str
    mode: str


@dataclass
class CleaningStartedEvent:
    robot_id: str


@dataclass
class CleaningStoppedEvent:
    robot_id: str


Event = Union[
    MovedEvent,
    TurnedEvent,
    ModeSetEvent,
    CleaningStartedEvent,
    CleaningStoppedEvent,
]


# мутабельный eventStore
class InMemoryEventStore:
    def __init__(self):
        self._events: List[Event] = []

    def append(self, event: Event) -> None:
        self._events.append(event)

    def append_many(self, events: List[Event]) -> None:
        self._events.extend(events)

    def load_for_robot(self, robot_id: str) -> List[Event]:
        return [event for event in self._events if event.robot_id == robot_id]

    def all_events(self) -> List[Event]:
        return list(self._events)
    


def no_transfer(_message):
    return None


def initial_robot_state() -> pure_robot.RobotState:
    return pure_robot.RobotState(
        0.0,
        0.0,
        0,
        pure_robot.WATER
    )


def apply_event(state: pure_robot.RobotState, event: Event) -> pure_robot.RobotState:
    if isinstance(event, MovedEvent):
        return pure_robot.move(no_transfer, event.distance, state)

    if isinstance(event, TurnedEvent):
        return pure_robot.turn(no_transfer, event.angle, state)

    if isinstance(event, ModeSetEvent):
        return pure_robot.set_state(no_transfer, event.mode, state)

    if isinstance(event, CleaningStartedEvent):
        return state

    if isinstance(event, CleaningStoppedEvent):
        return state

    raise ValueError(f"Unknown event: {event}")


def rebuild_state(events: List[Event]) -> pure_robot.RobotState:
    state = initial_robot_state()

    for event in events:
        state = apply_event(state, event)

    return state



def decide(command: Command, current_state: pure_robot.RobotState) -> List[Event]:

    if isinstance(command, MoveCommand):
        return [MovedEvent(command.robot_id, command.distance)]

    if isinstance(command, TurnCommand):
        return [TurnedEvent(command.robot_id, command.angle)]

    if isinstance(command, SetModeCommand):
        if command.mode not in ("water", "soap", "brush"):
            raise ValueError(f"Неподдерживаемый режим: {command.mode}")
        return [ModeSetEvent(command.robot_id, command.mode)]

    if isinstance(command, StartCleaningCommand):
        return [CleaningStartedEvent(command.robot_id)]

    if isinstance(command, StopCleaningCommand):
        return [CleaningStoppedEvent(command.robot_id)]

    raise ValueError(f"этой команды я не знаю: {command}")



class CommandHandler:
    def __init__(self, event_store: InMemoryEventStore):
        self.event_store = event_store

    def handle(self, command: Command) -> List[Event]:
        past_events = self.event_store.load_for_robot(command.robot_id)
        current_state = rebuild_state(past_events)

        new_events = decide(command, current_state)
        self.event_store.append_many(new_events)

        return new_events
    

def event_to_log_line(event: Event) -> str:
    if isinstance(event, MovedEvent):
        return f"MOVED {event.distance}"
    if isinstance(event, TurnedEvent):
        return f"TURNED {event.angle}"
    if isinstance(event, ModeSetEvent):
        return f"MODE_SET {event.mode}"
    if isinstance(event, CleaningStartedEvent):
        return "CLEANING_STARTED"
    if isinstance(event, CleaningStoppedEvent):
        return "CLEANING_STOPPED"
    return f"UNKNOWN_EVENT {event}"    


def build_log(events: List[Event]) -> List[str]:
    return [event_to_log_line(event) for event in events]
