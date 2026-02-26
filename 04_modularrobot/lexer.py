def lex(line: str) -> list[str]:
    line = line.strip()
    if not line:
        raise ValueError("command is empty")
    return line.split()
