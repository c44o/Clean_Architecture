import math
from typing import Optional 

def run(program_lines: list[str]) -> None:
    state = reset_to_initial()
    available_commands = bind_available_commands()
    for given_line in program_lines:
        given_command = parse_command(given_line)
        execute(state, available_commands, given_command)

state = {
    "x": 0.0,
    "y": 0.0,
    "angle": 0.0,
    "mode": "water", 
    "is_cleaning": False
}

def reset_to_initial() -> dict:
    return {
        "x": 0.0,
        "y": 0.0,
        "angle": 0.0,
        "mode": "water", 
        "is_clearning": False
    }

def bind_available_commands() -> dict:
    return {
        "move": move_robot,
        "turn": turn_robot,
        "set": set_robot_mode,
        "start": start_given_mode,
        "stop": stop_given_mode
    }

def execute(state: dict, commands: dict, given_command) -> None:
    commands[given_command["name"]](state, given_command["arg"])


def move_robot(state: dict, distance: float) -> dict:
    radians = math.radians(state["angle"])
    new_state = {}
    new_state["x"] += distance * math.cos(radians)
    new_state["y"] += distance * math.sin(radians)
    print(f"POS {new_state["x"]:.2f}, {new_state["y"]:.2f}")
    return new_state

def turn_robot(state: dict, rotation_angle: float) -> dict:
    state["angle"] = (state["angle"] + rotation_angle) % 360
    print(f"ANGLE {state["angle"]:.2f}")
    return state

def set_robot_mode(state: dict, mode: str) -> dict:
    state["mode"] = mode
    print(f"STATE {state["mode"]}")
    return state

def start_given_mode(state: dict, _=None) -> dict:
    state["is_cleaning"] = True
    print(f"START WITH {state["mode"]}")
    return state

def stop_given_mode(state: dict, _=None) -> dict:
    state["is_cleaning"] = False
    print(f"STOP")
    return state

def parse_command(line: str) -> dict:
    line = line.strip()
    if not line:
        raise ValueError("comand is empty")
    line_halves = line.split()
    command_name = line_halves[0].lower()

    if command_name not in ("move", "turn", "set", "start", "stop"):
        raise ValueError("command is unfamiliar")
    
    if command_name in ("start", "stop"):
        if len(line_halves) != 1:
            raise ValueError("command have no arguments")
        return {"name": command_name, "arg": None}
    
    if len(line_halves) != 2:
        raise ValueError("there is only one argument")
    
    if command_name in ('move', 'turn'): 
        try:
            command_arg = float(line_halves[1])
        except ValueError:
            raise ValueError(f"{line_halves[1]} is not compatible with move or turn commands")
        return {"name": command_name, "arg": command_arg}

    if command_name == "set":
        mode = line_halves[1].lower()
        if  mode not in ("water", "soap", "brush"):
            raise ValueError(f"{line_halves[1]} not applicable for mode command")
        return {"name": command_name, "arg": mode}



if __name__ == "__main__":
    test_program = ["move 100", "turn -90", "set soap", "start", "move 50", "stop"]
    run(test_program)

'''
## Робот-мойщик. Первая итерация

### Плюсы решения:
- не совсем спагетти-стиль. Функции не лежат по отдельности, завёрнуты в два класса плюс отдельные структуры данных для хранения состояния робота (class Robot) и чтобы переносить команду из одной функции в другую (dataclass Command).
- такой же лес if-else при разборе строки, но я бросаю исключения, в отличие от наивного решения
- его можно расширять до некоторой степени, опять-таки - потому, что логика кое-как разложена по классам, и на самом высоком уровне в коде всего три сущности (ровно те, которые запускаются из __main__ - Сommand, Interpreter, Robot)

### Минусы решения:
- всё равно довольно громоздко. 
- самое слабое место архтектурно - где сырую строку с командами надо разобрать и распределить по нужным функциям.
- возможно, стоило бы развести проверку корректности полученной строки, отдельно, и сопоставление разобранных команд с командами робота
- второе слабое место, здесь же - обработка в лоб разных типов полученной строки (без аргумента, с численным аргументом, со строковым аргументом). Работает, но выглядит неряшливо, и спустя день уже нужно заново разбираться, почему написано именно так
'''
