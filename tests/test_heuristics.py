
from collections import deque

import pytest

from srcs.heuristics.basic_heuristic import HeuristicFunction
from srcs.heuristics.manhattan_distance import ManhattanDistance
from srcs.heuristics.misplaced_tiles import MisplacedTiles
from srcs.heuristics.linear_conflict import LinearConflict
from tests.puzzle_states import GOALS


HEURISTICS = [
    ManhattanDistance,
    MisplacedTiles,
    LinearConflict,
]


@pytest.fixture(params=HEURISTICS, ids=lambda cls: cls.__name__)
def heuristic(request) -> HeuristicFunction:
    """Create a heuristic instance for each test."""
    instance = request.param()
    assert isinstance(instance, HeuristicFunction)
    return instance


def get_neighbors(state: tuple[int, ...], size: int):
    """Generate all states reachable by one legal move."""
    zero = state.index(0)
    row, col = divmod(zero, size)

    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        new_row = row + dr
        new_col = col + dc

        if not (0 <= new_row < size and 0 <= new_col < size):
            continue

        neighbor = list(state)
        target = new_row * size + new_col

        neighbor[zero], neighbor[target] = (
            neighbor[target], neighbor[zero]
        )

        yield tuple(neighbor)


def get_states_with_distances(goal, size, max_depth=5):
    """
    Use BFS to find states and their true shortest distances
    from the goal, up to max_depth moves.
    """
    distances = {goal: 0}
    queue = deque([goal])

    while queue:
        state = queue.popleft()
        distance = distances[state]

        if distance >= max_depth:
            continue

        for neighbor in get_neighbors(state, size):
            if neighbor in distances:
                continue

            distances[neighbor] = distance + 1
            queue.append(neighbor)

    return distances


@pytest.mark.parametrize("size", [3, 4, 5, 6])
def test_goal_returns_zero(heuristic, size):
    """The heuristic must return zero at the goal."""
    goal = GOALS[size]

    assert heuristic.calculate(goal, goal, size) == 0


@pytest.mark.parametrize("size", [3, 4, 5, 6])
def test_one_move_returns_one(heuristic, size):
    """One legal move from the goal should cost one."""
    goal = GOALS[size]
    state = next(get_neighbors(goal, size))

    assert heuristic.calculate(state, goal, size) == 1


@pytest.mark.parametrize("size", [3, 4, 5, 6])
def test_is_admissible(heuristic, size):
    """
    Check that h(state) never exceeds the true shortest
    distance for states reached by BFS.
    """
    goal = GOALS[size]
    distances = get_states_with_distances(
        goal, size, max_depth=5
    )

    for state, true_distance in distances.items():
        estimated = heuristic.calculate(state, goal, size)

        assert 0 <= estimated <= true_distance, (
            f"{type(heuristic).__name__}: "
            f"state={state}, "
            f"h={estimated}, "
            f"true_distance={true_distance}"
        )


@pytest.mark.parametrize("size", [3, 4, 5, 6])
def test_is_consistent(heuristic, size):
    """
    Check h(state) <= 1 + h(neighbor)
    for every tested legal transition.
    """
    goal = GOALS[size]
    distances = get_states_with_distances(
        goal, size, max_depth=5
    )

    for state in distances:
        h_current = heuristic.calculate(state, goal, size)

        for neighbor in get_neighbors(state, size):
            h_neighbor = heuristic.calculate(
                neighbor, goal, size
            )

            assert h_current <= 1 + h_neighbor, (
                f"{type(heuristic).__name__}: "
                f"state={state}, "
                f"neighbor={neighbor}, "
                f"h_current={h_current}, "
                f"h_neighbor={h_neighbor}"
            )


@pytest.mark.parametrize(
    "state, expected",
    [
        ((1, 2, 3, 8, 0, 4, 7, 6, 5), 0),
        ((1, 2, 3, 0, 8, 4, 7, 6, 5), 1),
        ((0, 2, 3, 1, 8, 4, 7, 6, 5), 2),
        ((2, 1, 3, 0, 8, 4, 5, 6, 7), 7),
        ((2, 1, 3, 0, 8, 4, 7, 6, 5), 3),
    ],
)
def test_manhattan_known_values(state, expected):
    """Preserve exact expected values for Manhattan Distance."""
    heuristic = ManhattanDistance()

    assert heuristic.calculate(state, GOALS[3], 3) == expected


def test_does_not_modify_input(heuristic):
    """Calculating a heuristic must not modify input states."""
    goal = GOALS[3]
    state = (2, 1, 3, 0, 8, 4, 5, 6, 7)

    original_state = state
    original_goal = goal

    heuristic.calculate(state, goal, 3)

    assert state == original_state
    assert goal == original_goal
