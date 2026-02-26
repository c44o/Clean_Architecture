from __future__ import annotations

import types
import dataclasses as BuildInDataClasses
from abc import ABC, abstractmethod
from typing import Any, Type

from domain import CleaningMode, Robot

class Command(ABC):
    @abstractmethod
    def execute(self, robot: Robot) -> None:
        ...

# здесь пробую ещё уменьшить избыточность и 
# создать метод-фабрику для создания команд-наследников\

def make_command_class(
        name: str,
        robot_method: str,
        fields: list[tuple[str, type]]
) -> Type[Command]:
    
    annotations = {fname: ftype for fname, ftype in fields}

    def execute(self, robot: Robot) -> None:
        args = [getattr(self, field_name) for field_name, _ in fields]
        getattr(robot, robot_method)(*args)
    
    blueprint_class = types.new_class(
        name,
        (Command,),
        {},
        lambda ns: ns.update({"__annotations__": annotations, "execute": execute}),
    )

    blueprint_class = BuildInDataClasses.dataclass(frozen=True)(blueprint_class)

    return blueprint_class

Move = make_command_class("Move", "move", [("distance", float)])
Turn = make_command_class("Turn", "turn", [("rotation_angle", float)])
Set  = make_command_class("Set", "set_mode", [("mode", CleaningMode)])
Start = make_command_class("Start", "start", [])
Stop  = make_command_class("Stop", "stop", [])
