from pathlib import Path
from srcs.heuristics.basic_heuristic import HeuristicFunction


def parse_puzzle_file(path: str | Path) -> tuple[int, tuple[int, ...]]:
    """Return (size, state) from a file, raising ValueError for invalid boards.

    The first nonempty, noncomment line is the board size. Subsequent lines
    contain rows of numbers. Comments start with '#', including inline comments.
    """
    lines = []
    with open(path, encoding="utf-8") as file:
        for line in file:
            content = line.split("#", 1)[0].strip()
            if content:
                lines.append(content)

    if not lines:
        raise ValueError("Puzzle file is empty")

    try:
        size = int(lines[0])
    except ValueError as exc:
        raise ValueError("First noncomment line must be an integer size") from exc

    if size < 3:
        raise ValueError("Board size must be at least 3")
    if len(lines) - 1 != size:
        raise ValueError(f"Expected {size} board rows, got {len(lines) - 1}")

    values: list[int] = []
    for row_number, line in enumerate(lines[1:], start=1):
        parts = line.split()
        if len(parts) != size:
            raise ValueError(
                f"Row {row_number} must contain {size} numbers, got {len(parts)}"
            )
        try:
            values.extend(int(token) for token in parts)
        except ValueError as exc:
            raise ValueError(f"Row {row_number} contains a noninteger tile") from exc

    expected = set(range(size * size))
    if set(values) != expected:
        raise ValueError(f"Tiles must contain every integer from 0 to {size * size - 1} exactly once")

    return size, tuple(values)
