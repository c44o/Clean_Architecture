```python
#func_dependecy_inection.py

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

#main.py

import pure_robot
from func_dependency_injection_08 import run_program

def transfer(message):
    print(message)

testing_robot_path_program = (
    "move 100",
    "turn -90",
    "set soap",
    "start", 
    "move 50",
    "stop"
)

initial_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

resulting_state = run_program(
    transfer, 
    testing_robot_path_program, 
    initial_state,
    move_functional=pure_robot.move,
    turn_functional=pure_robot.turn,
    set_functional=pure_robot.set_state,
    start_functional=pure_robot.start,
    stop_functional=pure_robot.stop,
)

print(resulting_state.x, resulting_state.y, resulting_state.angle, resulting_state.state)

#pure_robot.py
import math
from collections import namedtuple

RobotState = namedtuple("RobotState", "x y angle state")

# режимы работы устройства очистки
WATER = 1 # полив водой
SOAP  = 2 # полив мыльной пеной
BRUSH = 3 # чистка щётками


# взаимодействие с роботом вынесено в отдельную функцию
def transfer_to_cleaner(message):
    print (message)

# перемещение
def move(transfer,dist,state):
    angle_rads = state.angle * (math.pi/180.0)   
    new_state = RobotState(
        state.x + dist * math.cos(angle_rads),
        state.y + dist * math.sin(angle_rads),
        state.angle,
        state.state)  
    transfer(('POS(',new_state.x,',',new_state.y,')'))
    return new_state

# поворот
def turn(transfer,turn_angle,state):
    new_state = RobotState(
        state.x,
        state.y,
        state.angle + turn_angle,
        state.state)
    transfer(('ANGLE',state.angle))
    return new_state

# установка режима работы
def set_state(transfer,new_internal_state,state):
    if new_internal_state=='water':
        self_state = WATER  
    elif new_internal_state=='soap':
        self_state = SOAP
    elif new_internal_state=='brush':
        self_state = BRUSH
    else:
        return state  
    new_state = RobotState(
        state.x,
        state.y,
        state.angle,
        self_state)
    transfer(('STATE',self_state))
    return new_state

# начало чистки
def start(transfer,state):
    transfer(('START WITH',state.state))
    return state

# конец чистки
def stop(transfer,state):
    transfer(('STOP',))
    return state


# интерпретация набора команд
def make(transfer,code,state):
    for command in code:
        cmd = command.split(' ')
        if cmd[0]=='move':
            state = move(transfer,int(cmd[1]),state) 
        elif cmd[0]=='turn':
            state = turn(transfer,int(cmd[1]),state)
        elif cmd[0]=='set':
            state = set_state(transfer,cmd[1],state) 
        elif cmd[0]=='start':
            state = start(transfer,state)
        elif cmd[0]=='stop':
            state = stop(transfer,state)
    return state
    ```
