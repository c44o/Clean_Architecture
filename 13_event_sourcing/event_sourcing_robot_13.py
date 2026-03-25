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
