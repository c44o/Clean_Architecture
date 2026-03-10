from __future__ import annotations
from typing import Callable, Any

State = Any
Transfer = Callable[[Any], None]

Move_functional = Callable[[Transfer, int, State], State]
Turn_functional = Callable[[Transfer, int, State], State]
Set_functional = Callable[[Transfer, str, State], State]
Start_functional = Callable[[Transfer, State], State]
Stop_functional = Callable[[Transfer, State], State]

def run_program(
        transfer: Transfer, 
        code_to_execute: tuple[str, ...],
        state: State,
        move_functional: Move_functional,
        turn_functional: Turn_functional,
        set_functional: Set_functional,
        start_functional: Start_functional,
        stop_functional: Stop_functional
) -> State:
    for line in code_to_execute:
        parts = line.split()
        option = parts[0].lower()

        if option == "move":
            state = move_functional(transfer, int(parts[1]), state)
        elif option == "turn":
            state = turn_functional(transfer, int(parts[1]), state)
        elif option == "set":
            state = set_functional(transfer, parts[1], state)
        elif option == "start":
            state = start_functional(transfer, state)
        elif option == "stop":
            state = stop_functional(transfer, state)
        else:
            raise ValueError(f"{option}- какая-то непонятная команда")
        
    return state
