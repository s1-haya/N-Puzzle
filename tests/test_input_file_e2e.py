"""End-to-end tests of the actual N-Puzzle executable using .txt files.

Run from project root:
    make
    python3 -m pytest tests/test_input_file_e2e.py -v

Override executable:
    NPUZZLE_EXECUTABLE=./n_puzzle python3 -m pytest tests/test_input_file_e2e.py -v

No application code is imported: every case executes the CLI in a child process.
"""

import os
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
VALID = ROOT / "tests" / "input" / "parser_valid"
INVALID = ROOT / "tests" / "input" / "parser_invalid"


def snail_goal(size: int) -> tuple[int, ...]:
    """Compute the expected goal independently of the application's code."""
    board = [[-1] * size for _ in range(size)]
    top, bottom, left, right = 0, size - 1, 0, size - 1
    value = 1
    while left <= right and top <= bottom:
        for c in range(left, right + 1):
            board[top][c] = value
            value += 1
        top += 1
        for r in range(top, bottom + 1):
            board[r][right] = value
            value += 1
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):
                board[bottom][c] = value
                value += 1
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):
                board[r][left] = value
                value += 1
            left += 1
    return tuple(value if value != size * size else 0 for row in board for value in row)


def executable() -> Path:
    configured = os.environ.get("NPUZZLE_EXECUTABLE")
    if configured:
        target = Path(configured)
        return target if target.is_absolute() else ROOT / target
    for filename in ("n-puzzle", "n_puzzle"):
        target = ROOT / filename
        if target.is_file():
            return target
    pytest.fail("Executable not found: run `make` or set NPUZZLE_EXECUTABLE")


def run_cli(filename: Path, heuristic: str = "manhattan", timeout: int = 30):
    command = [str(executable()), f"--input={filename}", f"--heuristic={heuristic}"]
    try:
        return subprocess.run(command, cwd=ROOT, text=True, capture_output=True,
                              timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        pytest.fail(f"E2E command exceeded {timeout}s: {' '.join(command)}")


def assert_start_board(output: str, size: int, expected: tuple[int, ...]):
    """Check that CLI's displayed Start board matches the input, including order."""
    lines = output.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == "Start:":
            board_lines = lines[index + 1:index + 1 + size]
            assert len(board_lines) == size, f"Missing board rows:\n{output}"
            rows = [row.split() for row in board_lines]
            assert all(len(row) == size for row in rows), f"Wrong board dimensions:\n{output}"
            actual = tuple(int(tile) for row in rows for tile in row)
            assert actual == expected, f"Expected {expected}, got {actual}"
            return
    pytest.fail(f"Expected a 'Start:' board in program output:\n{output}")


def read_state_from_fixture(path: Path, size: int) -> tuple[int, ...]:
    """Read expected fixture data without importing the application parser."""
    lines = [line.split("#", 1)[0].strip() for line in path.read_text().splitlines()]
    meaningful = [line for line in lines if line]
    assert meaningful[0] == str(size), "Broken test fixture: wrong declared size"
    rows = [line.split() for line in meaningful[1:]]
    assert len(rows) == size and all(len(row) == size for row in rows)
    values = tuple(int(tile) for row in rows for tile in row)
    assert set(values) == set(range(size * size)), "Broken fixture: duplicate/missing tiles"
    return values


def assert_success(result, size, start, moves=None):
    output = result.stdout + "\n" + result.stderr
    assert result.returncode == 0, output
    assert_start_board(result.stdout, size, start)
    assert "Goal reached!" in result.stdout, output
    assert "Complexity in time:" in result.stdout, output
    assert "Complexity in size:" in result.stdout, output
    match = re.search(r"Number of moves:\s*(\d+)", result.stdout)
    assert match is not None, output
    if moves is not None:
        assert int(match.group(1)) == moves, output
    assert "The ordered sequence of states" in result.stdout, output
    assert str(snail_goal(size)) in result.stdout, "Final snail goal was not printed"


# Original 3x3 cases are preserved.
THREE_BY_THREE_VALID = [
    ("valid_basic.txt", "solved"),
    ("valid_comments.txt", "solved"),
    ("valid_two_spaces.txt", "solved"),
    ("valid_blank_lines.txt", "solved"),
    ("valid_order_not_sorted.txt", "solved"),
    ("valid_unsolvable_but_well_formed.txt", "unsolvable"),
    ("valid_multiple_spaces.txt", "solved"),
]


@pytest.mark.parametrize("filename,outcome", THREE_BY_THREE_VALID)
def test_3x3_existing_cases(filename, outcome):
    path = VALID / filename
    start = read_state_from_fixture(path, 3)
    result = run_cli(path)
    if outcome == "unsolvable":
        output = result.stdout + result.stderr
        assert "not solvable" in output.lower() or "unsolvable" in output.lower(), output
        assert "Goal reached!" not in output
    else:
        assert_success(result, 3, start, moves=0 if filename == "valid_multiple_spaces.txt" else None)


@pytest.mark.parametrize("size", [4, 5, 17])
@pytest.mark.parametrize("kind,moves", [("solved", 0), ("one_move", 1)])
def test_large_board_solved_and_one_move(size, kind, moves):
    """Full file->CLI->search->stats->solution workflow, including 17x17."""
    path = VALID / f"valid_{size}x{size}_{kind}.txt"
    start = read_state_from_fixture(path, size)
    assert_success(run_cli(path, timeout=40), size, start, moves=moves)


@pytest.mark.parametrize("size", [4, 5, 17])
@pytest.mark.parametrize("kind", ["comments", "multiple_spaces", "aligned"])
def test_large_board_format_variations(size, kind):
    """Accept inline comments, aligned rows and 3+ spaces at every size."""
    path = VALID / f"valid_{size}x{size}_{kind}.txt"
    start = read_state_from_fixture(path, size)
    assert_success(run_cli(path, timeout=40), size, start, moves=0)


@pytest.mark.parametrize("size", [4, 5, 17])
def test_large_board_well_formed_but_unsolvable(size):
    """File is valid, but swapping two nonblank tiles makes it unreachable."""
    path = VALID / f"valid_{size}x{size}_unsolvable.txt"
    result = run_cli(path, timeout=40)
    output = result.stdout + "\n" + result.stderr
    assert "not solvable" in output.lower() or "unsolvable" in output.lower(), output
    assert "Goal reached!" not in output


THREE_BY_THREE_INVALID = [
    "invalid_size_2.txt", "invalid_size_not_integer.txt", "invalid_size_row_mismatch.txt",
    "invalid_too_few_rows.txt", "invalid_too_many_rows.txt", "invalid_too_few_columns.txt",
    "invalid_too_many_columns.txt", "invalid_duplicate_tile.txt", "invalid_negative_tile.txt",
    "invalid_tile_9.txt", "invalid_nonnumeric_tile.txt", "invalid_extra_token.txt",
    "invalid_uncommented_number.txt", "invalid_empty.txt", "invalid_fraction_size.txt",
]


@pytest.mark.parametrize("filename", THREE_BY_THREE_INVALID)
def test_3x3_invalid_input_rejected(filename):
    result = run_cli(INVALID / filename)
    assert result.returncode != 0, result.stdout + result.stderr
    assert "Goal reached!" not in result.stdout


@pytest.mark.parametrize("size", [4, 5, 17])
@pytest.mark.parametrize("kind", [
    "duplicate", "out_of_range", "few_columns", "extra_columns",
    "few_rows", "extra_rows", "nonnumeric", "uncommented_number",
])
def test_large_board_invalid_input_rejected(size, kind):
    result = run_cli(INVALID / f"invalid_{size}x{size}_{kind}.txt", timeout=40)
    assert result.returncode != 0, result.stdout + result.stderr
    assert "Goal reached!" not in result.stdout


@pytest.mark.parametrize("size", [3, 4, 5, 17])
def test_nonexistent_file_rejected(size):
    result = run_cli(INVALID / f"does_not_exist_{size}.txt")
    assert result.returncode != 0, result.stdout + result.stderr


@pytest.mark.parametrize("size", [3, 4, 5])
@pytest.mark.parametrize("heuristic", ["manhattan", "misplaced", "linear_conflict"])
def test_heuristic_cli_option(size, heuristic):
    """All three heuristics must work on a solved state (no expensive search)."""
    if size == 3:
        path = VALID / "valid_multiple_spaces.txt"
    else:
        path = VALID / f"valid_{size}x{size}_solved.txt"
    start = read_state_from_fixture(path, size)
    assert_success(run_cli(path, heuristic=heuristic), size, start, moves=0)


def test_invalid_heuristic_rejected():
    result = run_cli(VALID / "valid_basic.txt", heuristic="does_not_exist")
    assert result.returncode != 0, result.stdout + result.stderr
