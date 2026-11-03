
import unittest

from srcs.heuristics.manhattan_distance import ManhattanDistance


class TestManhattanDistance(unittest.TestCase):

    def setUp(self):
        """Prepare a fresh heuristic for each test."""
        self.heuristic = ManhattanDistance()
        self.goal = (1, 2, 3, 8, 0, 4, 7, 6, 5)

    def test_goal_state_returns_zero(self):
        result = self.heuristic.calculate(
            self.goal, self.goal, 3
        )
        self.assertEqual(result, 0)

    def test_one_move_returns_one(self):
        state = (1, 2, 3, 0, 8, 4, 7, 6, 5)

        result = self.heuristic.calculate(
            state, self.goal, 3
        )
        self.assertEqual(result, 1)

    def test_two_moves_returns_two(self):
        state = (0, 2, 3, 1, 8, 4, 7, 6, 5)

        result = self.heuristic.calculate(
            state, self.goal, 3
        )
        self.assertEqual(result, 2)

    def test_multiple_displaced_tiles(self):
        state = (2, 1, 3, 0, 8, 4, 5, 6, 7)

        result = self.heuristic.calculate(
            state, self.goal, 3
        )
        self.assertEqual(result, 7)

    def test_original_tuple(self):
        state = (2, 1, 3, 0, 8, 4, 7, 6, 5)

        result = self.heuristic.calculate(
            state, self.goal, 3
        )
        self.assertEqual(result, 3)

    def test_four_by_four_board(self):
        goal = (
            1,  2,  3,  4,
            12, 13, 14, 5,
            11, 0,  15, 6,
            10, 9,  8,  7,
        )
        state = (
            1,  2,  3,  4,
            12, 0,  14, 5,
            11, 13, 15, 6,
            10, 9,  8,  7,
        )

        result = self.heuristic.calculate(
            state, goal, 4
        )
        self.assertEqual(result, 1)

    def test_does_not_modify_input(self):
        state = (2, 1, 3, 0, 8, 4, 5, 6, 7)
        original_state = state
        original_goal = self.goal

        self.heuristic.calculate(state, self.goal, 3)

        self.assertEqual(state, original_state)
        self.assertEqual(self.goal, original_goal)


if __name__ == "__main__":
    unittest.main()
