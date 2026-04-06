from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Callable, List, Tuple, Optional
import pure_robot



@dataclass(frozen=True)
class MoveResponse:
    distance: float
    ok: bool


@dataclass(frozen=True)
class TurnResponse:
    angle: float
    ok: bool


@dataclass(frozen=True)
class StateResponse:
    mode: str
    ok: bool


@dataclass(frozen=True)
class StartResponse:
    ok: bool


# базовый узел
class AstNode(ABC):
    @abstractmethod
    def interpret(
        self,
        interpreter: "RobotInterpreter",
        state: pure_robot.RobotState
    ) -> pure_robot.RobotState:
        pass



#узел окончания
@dataclass(frozen=True)
class Stop(AstNode):
    def interpret(
        self,
        interpreter: "RobotInterpreter",
        state: pure_robot.RobotState
    ) -> pure_robot.RobotState:
        return interpreter.execute_stop(state)



# промежуточные узлы
@dataclass(frozen=True)
class Move(AstNode):
    distance: float
    next: Callable[[MoveResponse], AstNode]

    def interpret(
        self,
        interpreter: "RobotInterpreter",
        state: pure_robot.RobotState
    ) -> pure_robot.RobotState:
        new_state, response = interpreter.execute_move(state, self.distance)
        next_node = self.next(response)
        return next_node.interpret(interpreter, new_state)


@dataclass(frozen=True)
class Turn(AstNode):
    angle: float
    next: Callable[[TurnResponse], AstNode]

    def interpret(
        self,
        interpreter: "RobotInterpreter",
        state: pure_robot.RobotState
    ) -> pure_robot.RobotState:
        new_state, response = interpreter.execute_turn(state, self.angle)
        next_node = self.next(response)
        return next_node.interpret(interpreter, new_state)


@dataclass(frozen=True)
class SetState(AstNode):
    mode: str
    next: Callable[[StateResponse], AstNode]

    def interpret(
        self,
        interpreter: "RobotInterpreter",
        state: pure_robot.RobotState
    ) -> pure_robot.RobotState:
        new_state, response = interpreter.execute_set_state(state, self.mode)
        next_node = self.next(response)
        return next_node.interpret(interpreter, new_state)


@dataclass(frozen=True)
class Start(AstNode):
    next: Callable[[StartResponse], AstNode]

    def interpret(
        self,
        interpreter: "RobotInterpreter",
        state: pure_robot.RobotState
    ) -> pure_robot.RobotState:
        new_state, response = interpreter.execute_start(state)
        next_node = self.next(response)
        return next_node.interpret(interpreter, new_state)


# интерпретатор
class RobotInterpreter:
    def __init__(self, transfer=None):
        self.messages: List[object] = []
        self.transfer = transfer or self._collect_transfer

    def _collect_transfer(self, message):
        self.messages.append(message)
        print(message)

    def initial_state(self) -> pure_robot.RobotState:
        return pure_robot.RobotState(
            0.0,
            0.0,
            0,
            pure_robot.WATER
        )

    def run(
        self,
        program: AstNode,
        initial_state: Optional[pure_robot.RobotState] = None
    ) -> Tuple[pure_robot.RobotState, List[object]]:
        self.messages = []

        if initial_state is None:
            initial_state = self.initial_state()

        final_state = program.interpret(self, initial_state)
        return final_state, self.messages

    def execute_move(
        self,
        state: pure_robot.RobotState,
        distance: float
    ) -> Tuple[pure_robot.RobotState, MoveResponse]:
        new_state = pure_robot.move(self.transfer, distance, state)
        response = MoveResponse(distance=distance, ok=True)
        return new_state, response

    def execute_turn(
        self,
        state: pure_robot.RobotState,
        angle: float
    ) -> Tuple[pure_robot.RobotState, TurnResponse]:
        new_state = pure_robot.turn(self.transfer, angle, state)
        response = TurnResponse(angle=angle, ok=True)
        return new_state, response

    def execute_set_state(
        self,
        state: pure_robot.RobotState,
        mode: str
    ) -> Tuple[pure_robot.RobotState, StateResponse]:
        new_state = pure_robot.set_state(self.transfer, mode, state)
        response = StateResponse(mode=mode, ok=True)
        return new_state, response

    def execute_start(
        self,
        state: pure_robot.RobotState
    ) -> Tuple[pure_robot.RobotState, StartResponse]:
        new_state = pure_robot.start(self.transfer, state)
        response = StartResponse(ok=True)
        return new_state, response

    def execute_stop(
        self,
        state: pure_robot.RobotState
    ) -> pure_robot.RobotState:
        return pure_robot.stop(self.transfer, state)
