import pytest

from srcs.astar import AStar
from srcs.heuristics.manhattan_distance import ManhattanDistance
from tests.puzzle_states import GOALS, swap_tiles



import pytest

from srcs.astar import AStar
from srcs.heuristics.manhattan_distance import ManhattanDistance
from tests.puzzle_states import GOALS, swap_tiles


@pytest.mark.parametrize("size", [3, 4, 5, 6])
def test_already_solved(size):
    """The goal state must be reachable from itself."""
    goal = GOALS[size]

    solver = AStar(
        start=goal,
        goal=goal,
        size=size,
        heuristic=ManhattanDistance(),
    )

    assert solver._is_solvable() is True


@pytest.mark.parametrize(
    "size, blank_index, neighbor_index",
    [
        # 3x3
        pytest.param(3, 4, 1, id="3x3_vertical"),
        pytest.param(3, 4, 3, id="3x3_horizontal"),

        # 4x4
        pytest.param(4, 9, 5, id="4x4_vertical"),
        pytest.param(4, 9, 10, id="4x4_horizontal"),

        # 5x5
        pytest.param(5, 12, 7, id="5x5_vertical"),
        pytest.param(5, 12, 13, id="5x5_horizontal"),

        # 6x6
        pytest.param(6, 20, 14, id="6x6_vertical"),
        pytest.param(6, 20, 21, id="6x6_horizontal"),
    ],
)
def test_legal_move_is_solvable(size, blank_index, neighbor_index):
    """One legal move from the goal must remain solvable."""
    goal = GOALS[size]
    start = swap_tiles(goal, blank_index, neighbor_index)

    solver = AStar(
        start=start,
        goal=goal,
        size=size,
        heuristic=ManhattanDistance(),
    )

    assert solver._is_solvable() is True


@pytest.mark.parametrize("size", [3, 4, 5, 6])
def test_swapped_numbered_tiles_are_unsolvable(size):
    """Swapping two numbered tiles changes solvability parity."""
    goal = GOALS[size]
    start = swap_tiles(goal, 0, 1)

    solver = AStar(
        start=start,
        goal=goal,
        size=size,
        heuristic=ManhattanDistance(),
    )

    assert solver._is_solvable() is False
