
import unittest

from srcs.astar import AStar
from srcs.heuristics.manhattan_distance import ManhattanDistance


class TestGetNeighbors(unittest.TestCase):

    def setUp(self):
        self.goal = (1, 2, 3, 8, 0, 4, 7, 6, 5)
        self.solver = AStar(
            start=self.goal,
            goal=self.goal,
            size=3,
            heuristic=ManhattanDistance(),
        )

    def test_corner_has_two_neighbors(self):
        state = (0, 1, 2, 3, 4, 5, 6, 7, 8)

        expected = {
            (1, 0, 2, 3, 4, 5, 6, 7, 8),  # Right
            (3, 1, 2, 0, 4, 5, 6, 7, 8),  # Down
        }

        neighbors = self.solver._get_neighbors(state)

        self.assertEqual(set(neighbors), expected)
        self.assertEqual(len(neighbors), 2)

    def test_edge_has_three_neighbors(self):
        state = (1, 0, 2, 3, 4, 5, 6, 7, 8)

        expected = {
            (0, 1, 2, 3, 4, 5, 6, 7, 8),  # Left
            (1, 2, 0, 3, 4, 5, 6, 7, 8),  # Right
            (1, 4, 2, 3, 0, 5, 6, 7, 8),  # Down
        }

        neighbors = self.solver._get_neighbors(state)

        self.assertEqual(set(neighbors), expected)
        self.assertEqual(len(neighbors), 3)

    def test_center_has_four_neighbors(self):
        state = (1, 2, 3, 8, 0, 4, 7, 6, 5)

        expected = {
            (1, 0, 3, 8, 2, 4, 7, 6, 5),  # Up
            (1, 2, 3, 8, 6, 4, 7, 0, 5),  # Down
            (1, 2, 3, 0, 8, 4, 7, 6, 5),  # Left
            (1, 2, 3, 8, 4, 0, 7, 6, 5),  # Right
        }

        neighbors = self.solver._get_neighbors(state)

        self.assertEqual(set(neighbors), expected)
        self.assertEqual(len(neighbors), 4)

    def test_does_not_modify_original_state(self):
        state = (1, 2, 3, 8, 0, 4, 7, 6, 5)
        original = state

        self.solver._get_neighbors(state)

        self.assertEqual(state, original)

    def test_no_duplicate_neighbors(self):
        state = (1, 2, 3, 8, 0, 4, 7, 6, 5)

        neighbors = self.solver._get_neighbors(state)

        self.assertEqual(len(neighbors), len(set(neighbors)))

    def test_all_neighbors_are_legal_moves(self):
        state = (1, 2, 3, 8, 0, 4, 7, 6, 5)

        neighbors = self.solver._get_neighbors(state)

        for neighbor in neighbors:
            with self.subTest(neighbor=neighbor):
                self.assertTrue(
                    self._is_valid_move(state, neighbor, 3)
                )

    @staticmethod
    def _is_valid_move(current, neighbor, size):
        if len(current) != size * size:
            return False
        if len(neighbor) != len(current):
            return False
        if set(current) != set(range(size * size)):
            return False
        if set(neighbor) != set(range(size * size)):
            return False

        old_zero = current.index(0)
        new_zero = neighbor.index(0)

        old_row, old_col = divmod(old_zero, size)
        new_row, new_col = divmod(new_zero, size)

        distance = (
            abs(old_row - new_row)
            + abs(old_col - new_col)
        )
        if distance != 1:
            return False

        changed = {
            i for i in range(len(current))
            if current[i] != neighbor[i]
        }

        return (
            changed == {old_zero, new_zero}
            and neighbor[old_zero] == current[new_zero]
            and neighbor[new_zero] == 0
        )


if __name__ == "__main__":
    unittest.main()
