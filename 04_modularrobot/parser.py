from __future__ import annotations

from dataclasses import dataclass

from commands import Command, Move, Turn, Set, Start, Stop
from domain import CleaningMode
from lexer import lex


@dataclass(frozen=True)
class Parsed:
    name: str
    arg: str | None


def parse_syntax(tokens: list[str]) -> Parsed:
    name = tokens[0].lower()

    if name in ("start", "stop"):
        if len(tokens) != 1:
            raise ValueError(f"'{name}' takes no arguments")
        return Parsed(name=name, arg=None)

    if len(tokens) != 2:
        raise ValueError(f"'{name}' expects exactly 1 argument")

    return Parsed(name=name, arg=tokens[1])


def parse_semantics(p: Parsed) -> Command:
    if p.name == "start":
        return Start()
    if p.name == "stop":
        return Stop()

    assert p.arg is not None

    if p.name == "move":
        try:
            return Move(float(p.arg))
        except ValueError:
            raise ValueError(f"'move' expects a number, got: {p.arg}")

    if p.name == "turn":
        try:
            return Turn(float(p.arg))
        except ValueError:
            raise ValueError(f"'turn' expects a number, got: {p.arg}")

    if p.name == "set":
        mode = p.arg.lower()
        try:
            return Set(CleaningMode(mode))
        except ValueError:
            raise ValueError(f"'set' expects water/soap/brush, got: {p.arg}")

    raise ValueError(f"command is unfamiliar: {p.name}")


def parse_command(line: str) -> Command:
    tokens = lex(line)
    parsed = parse_syntax(tokens)
    return parse_semantics(parsed)
