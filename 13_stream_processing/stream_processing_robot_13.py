from dataclasses import dataclass
from typing import List, Protocol, Union, Dict
import pure_robot

# команды
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
    StopCleaningCommand,
]

# запросы
@dataclass
class MoveRequestedEvent:
    robot_id: str
    distance: float

@dataclass
class TurnRequestedEvent:
    robot_id: str
    angle: float

@dataclass
class SetModeRequestedEvent:
    robot_id: str
    mode: str

@dataclass
class CleaningStartRequestedEvent:
    robot_id: str

@dataclass
class CleaningStopRequestedEvent:
    robot_id: str


# результаты

@dataclass
class RobotMovedEvent:
    robot_id: str
    distance: float

@dataclass
class RobotTurnedEvent:
    robot_id: str
    angle: float 

@dataclass
class RobotModeSetEvent:
    robot_id: str
    mode: str

@dataclass
class RobotStartedCleaningEvent:
    robot_id: str

@dataclass
class RobotStoppedCleaningEvent:
    robot_id: str

Event = Union[
    MoveRequestedEvent,
    TurnRequestedEvent,
    SetModeRequestedEvent,
    CleaningStartRequestedEvent,
    CleaningStopRequestedEvent,
    RobotMovedEvent,
    RobotTurnedEvent,
    RobotMovedEvent,
    RobotModeSetEvent,
    RobotStartedCleaningEvent,
    RobotStoppedCleaningEvent
]


# Event stor

class EventSubscriber(Protocol):
    def handle_event(self, event: Event) -> None:
        ...


class EventStore:
    def __init__(self):
        self._events: Dict[str, List[Event]] = {}
        self._subscribers: List[EventSubscriber] = []

    def subscribe(self, subscriber: EventSubscriber) -> None:
        self._subscribers.append(subscriber)

    def append_event(self, event: Event) -> None:
        robot_id = event.robot_id
        if robot_id not in self._events:
            self._events[robot_id] = []

        self._events[robot_id].append(event)

        for subscriber in self._subscribers:
            subscriber.handle_event(event)

    def append_events(self, events: List[Event]) -> None:
        for event in events:
            self.append_event(event)

    def get_events(self, robot_id: str) -> List[Event]:
        return list(self._events.get(robot_id, []))
    

class StateProjector:
    def __init__(self, initial_state: pure_robot.RobotState):
        self._initial_state = initial_state

    def project_state(self, events: List[Event]) -> pure_robot.RobotState:
        state = self._initial_state

        for event in events:
            state = self.apply_event(state, event)

        return state

    def apply_event(
            self, 
            state: pure_robot.RobotState,
            event: Event
    ) -> pure_robot.RobotState:
        def no_transfer(_message):
            return None
        
        if isinstance(event, RobotMovedEvent):
            return pure_robot.move(no_transfer, event.distance, state)
        
        if isinstance(event, RobotTurnedEvent):
            return pure_robot.turn(no_transfer, event.angle, state)
        
        if isinstance(event, RobotModeSetEvent):
            return pure_robot.set_state(no_transfer, event.mode, state)

        if isinstance(event, RobotStartedCleaningEvent):
            return state
        
        if isinstance(event, RobotStoppedCleaningEvent):
            return state
        
        return state
    

class CommandHandler:
    def __init__(self, event_store: EventStore):
        self._event_store = event_store

    def handle_command(self, command: Command) -> None:
        request_event = self._to_requested_event(command)
        self._event_store.append_event(request_event)

    def _to_requested_event(self, command: Command) -> Event:
        if isinstance(command, MoveCommand):
            return MoveRequestedEvent(command.robot_id, command.distance)
        
        if isinstance(command, TurnCommand):
            return TurnRequestedEvent(command.robot_id, command.angle)
        
        if isinstance(command, SetModeCommand):
            if command.mode not in ("water", "soap", "brush"):
                raise ValueError(f"такого режима нет - {command.mode}")
            return SetModeRequestedEvent(command.robot_id, command.mode)
        
        if isinstance(command, StartCleaningCommand):
            return CleaningStartRequestedEvent(command.robot_id)
        
        if isinstance(command, StopCleaningCommand):
            return CleaningStopRequestedEvent(command.robot_id)
        
        raise ValueError(f"какая-то незнакомая команда - {command}")
    

# Event processor
class RobotEventProcessor:
    def __init__(self, event_store: EventStore, projector: StateProjector):
        self._event_store = event_store
        self._projector = projector

    def handle_event(self, event: Event) -> None:
        if isinstance(event, MoveRequestedEvent):
            self._handle_move_requested(event)
            return
        
        if isinstance(event, TurnRequestedEvent):
            self._handle_turn_requested(event)
            return
        
        if isinstance(event, SetModeRequestedEvent):
            self._handle_set_mode_requested(event)
            return

        if isinstance(event, CleaningStartRequestedEvent):
            self._handle_start_requested(event)
            return

        if isinstance(event, CleaningStopRequestedEvent):
            self._handle_stop_requested(event)
            return

    def _current_state(self, robot_id: str) -> pure_robot.RobotState:
        events = self._event_store.get_events(robot_id)
        return self._projector.project_state(events)

    def _handle_move_requested(self, event: MoveRequestedEvent) -> None:
        current_state = self._current_state(event.robot_id)

        # Здесь могла бы быть более сложная бизнес-логика
        if event.distance == 0:
            return

        result_event = RobotMovedEvent(event.robot_id, event.distance)
        self._event_store.append_event(result_event)

    def _handle_turn_requested(self, event: TurnRequestedEvent) -> None:
        current_state = self._current_state(event.robot_id)

        if event.angle == 0:
            return

        result_event = RobotTurnedEvent(event.robot_id, event.angle)
        self._event_store.append_event(result_event)

    def _handle_set_mode_requested(self, event: SetModeRequestedEvent) -> None:
        current_state = self._current_state(event.robot_id)

        result_event = RobotModeSetEvent(event.robot_id, event.mode)
        self._event_store.append_event(result_event)

    def _handle_start_requested(self, event: CleaningStartRequestedEvent) -> None:
        current_state = self._current_state(event.robot_id)

        result_event = RobotStartedCleaningEvent(event.robot_id)
        self._event_store.append_event(result_event)

    def _handle_stop_requested(self, event: CleaningStopRequestedEvent) -> None:
        current_state = self._current_state(event.robot_id)

        result_event = RobotStoppedCleaningEvent(event.robot_id)
        self._event_store.append_event(result_event) 

# вывод

def event_to_text(event: Event) -> str:
    if isinstance(event, MoveRequestedEvent):
        return f"MoveRequested({event.distance})"
    if isinstance(event, TurnRequestedEvent):
        return f"TurnRequested({event.angle})"
    if isinstance(event, SetModeRequestedEvent):
        return f"SetModeRequested({event.mode})"
    if isinstance(event, CleaningStartRequestedEvent):
        return "CleaningStartRequested"
    if isinstance(event, CleaningStopRequestedEvent):
        return "CleaningStopRequested"

    if isinstance(event, RobotMovedEvent):
        return f"RobotMoved({event.distance})"
    if isinstance(event, RobotTurnedEvent):
        return f"RobotTurned({event.angle})"
    if isinstance(event, RobotModeSetEvent):
        return f"RobotModeSet({event.mode})"
    if isinstance(event, RobotStartedCleaningEvent):
        return "RobotStartedCleaning"
    if isinstance(event, RobotStoppedCleaningEvent):
        return "RobotStoppedCleaning"

    return f"UnknownEvent({event})"
