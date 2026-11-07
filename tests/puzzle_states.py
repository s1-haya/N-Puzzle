"""Shared N-Puzzle board states for tests.

Import these constants from individual test modules to avoid repeating boards.
"""

GOAL_3X3 = (
    1, 2, 3,
    8, 0, 4,
    7, 6, 5,
)

GOAL_4X4 = (
    1, 2, 3, 4,
    12, 13, 14, 5,
    11, 0, 15, 6,
    10, 9, 8, 7,
)

GOAL_5X5 = (
    1, 2, 3, 4, 5,
    16, 17, 18, 19, 6,
    15, 24, 0, 20, 7,
    14, 23, 22, 21, 8,
    13, 12, 11, 10, 9,
)

GOAL_6X6 = (
    1, 2, 3, 4, 5, 6,
    20, 21, 22, 23, 24, 7,
    19, 32, 33, 34, 25, 8,
    18, 31, 0, 35, 26, 9,
    17, 30, 29, 28, 27, 10,
    16, 15, 14, 13, 12, 11,
)

GOALS = {
    3: GOAL_3X3,
    4: GOAL_4X4,
    5: GOAL_5X5,
    6: GOAL_6X6,
}


def swap_tiles(state: tuple[int, ...], i: int, j: int) -> tuple[int, ...]:
    """Make a new state with the tiles at positions i and j swapped."""
    tiles = list(state)
    tiles[i], tiles[j] = tiles[j], tiles[i]
    return tuple(tiles)
