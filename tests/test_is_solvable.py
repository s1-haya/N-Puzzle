
import pytest

from srcs.astar import AStar
from srcs.heuristics.manhattan_distance import ManhattanDistance
from srcs.heuristics.misplaced_tiles import MisplacedTiles
from srcs.heuristics.linear_conflict import LinearConflict
from tests.puzzle_states import GOALS, swap_tiles


HEURISTICS = [
    ManhattanDistance,
    MisplacedTiles,
    LinearConflict,
]


@pytest.fixture(params=HEURISTICS, ids=lambda cls: cls.__name__)
def heuristic(request):
    """Create each heuristic for the solvability tests."""
    return request.param()


def check_solvable(size, start, expected, heuristic):
    """Check solvability using the selected heuristic."""
    solver = AStar(
        start=start,
        goal=GOALS[size],
        size=size,
        heuristic=heuristic,
    )

    assert solver._is_solvable() is expected


@pytest.mark.parametrize("size", [3, 4, 5, 6])
def test_already_solved(size, heuristic):
    """The goal must be reachable from itself."""
    goal = GOALS[size]

    check_solvable(size, goal, True, heuristic)


@pytest.mark.parametrize(
    "size, blank_index, neighbor_index",
    [
        pytest.param(3, 4, 1, id="3x3_vertical"),
        pytest.param(3, 4, 3, id="3x3_horizontal"),
        pytest.param(4, 9, 5, id="4x4_vertical"),
        pytest.param(4, 9, 10, id="4x4_horizontal"),
        pytest.param(5, 12, 7, id="5x5_vertical"),
        pytest.param(5, 12, 13, id="5x5_horizontal"),
        pytest.param(6, 20, 14, id="6x6_vertical"),
        pytest.param(6, 20, 21, id="6x6_horizontal"),
    ],
)
def test_legal_move_is_solvable(
    size, blank_index, neighbor_index, heuristic
):
    """A legal move from the goal preserves solvability."""
    goal = GOALS[size]
    start = swap_tiles(goal, blank_index, neighbor_index)

    check_solvable(size, start, True, heuristic)


@pytest.mark.parametrize("size", [3, 4, 5, 6])
def test_swapped_numbered_tiles_are_unsolvable(size, heuristic):
    """Exchanging two numbered tiles makes the goal unreachable."""
    goal = GOALS[size]
    start = swap_tiles(goal, 0, 1)

    check_solvable(size, start, False, heuristic)


@pytest.mark.parametrize(
    "start, expected",
    [
        pytest.param(
            (8, 6, 7, 2, 0, 5, 3, 4, 1),
            True,
            id="hard_3x3_same_parity",
        ),
        pytest.param(
            (3, 2, 1, 4, 0, 8, 5, 7, 6),
            True,
            id="different_counts_same_parity",
        ),
        pytest.param(
            (1, 2, 3, 4, 0, 8, 7, 6, 5),
            False,
            id="different_parity",
        ),
        pytest.param(
            (2, 1, 3, 8, 0, 4, 7, 6, 5),
            False,
            id="swapped_tiles",
        ),
    ],
)
def test_additional_3x3_states(start, expected, heuristic):
    """Check additional solvable and unsolvable states."""
    check_solvable(3, start, expected, heuristic)
