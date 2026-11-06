
import unittest

from srcs.astar import AStar
from srcs.heuristics.manhattan_distance import ManhattanDistance

from math import isqrt


class TestIsSolvable(unittest.TestCase):

    def setUp(self):
        self.goal_3x3 = (
            1, 2, 3,
            8, 0, 4,
            7, 6, 5,
        )

        self.goal_4x4 = (
            1, 2, 3, 4,
            12, 13, 14, 5,
            11, 0, 15, 6,
            10, 9, 8, 7,
        )
 
        self.goal_5x5 = (
            1, 2, 3, 4, 5,
            16, 17, 18, 19, 6,
            15, 24, 0, 20, 7,
            14, 23, 22, 21, 8,
            13, 12, 11, 10, 9,
        )

        self.goal_6x6 = (
            1, 2, 3, 4, 5, 6,
            20, 21, 22, 23, 24, 7,
            19, 32, 33, 34, 25, 8,
            18, 31, 0, 35, 26, 9,
            17, 30, 29, 28, 27, 10,
            16, 15, 14, 13, 12, 11,
        )

    def check_solvable(self, start, goal, expected):
        # Adjust constructor arguments if necessary.
        solver = AStar(
            start=start,
            goal=goal,
            size=isqrt(len(goal)),
            heuristic=ManhattanDistance(),
        )
        self.assertEqual(solver._is_solvable(), expected)

    def test_already_solved_3x3(self):
        self.check_solvable(
            self.goal_3x3, self.goal_3x3, True
        )

    def test_one_move_3x3(self):
        start = (
            1, 2, 3,
            0, 8, 4,
            7, 6, 5,
        )
        self.check_solvable(start, self.goal_3x3, True)

    def test_same_odd_parity_3x3(self):
        start = (
            3, 2, 1,
            4, 0, 8,
            5, 7, 6,
        )
        self.check_solvable(start, self.goal_3x3, True)

    def test_different_parity_3x3(self):
        start = (
            1, 2, 3,
            4, 0, 8,
            7, 6, 5,
        )
        self.check_solvable(start, self.goal_3x3, False)

    def test_swapped_tiles_3x3(self):
        start = (
            2, 1, 3,
            8, 0, 4,
            7, 6, 5,
        )
        self.check_solvable(start, self.goal_3x3, False)

    def test_already_solved_4x4(self):
        self.check_solvable(
            self.goal_4x4, self.goal_4x4, True
        )

    def test_one_vertical_move_4x4(self):
        start = (
            1, 2, 3, 4,
            12, 0, 14, 5,
            11, 13, 15, 6,
            10, 9, 8, 7,
        )
        self.check_solvable(start, self.goal_4x4, True)

    def test_swapped_tiles_4x4(self):
        start = (
            2, 1, 3, 4,
            12, 13, 14, 5,
            11, 0, 15, 6,
            10, 9, 8, 7,
        )
        self.check_solvable(start, self.goal_4x4, False)
    

    # -------------------------
    # 5x5 tests (odd-sized)
    # -------------------------

    def test_already_solved_5x5(self):
        self.check_solvable(
            self.goal_5x5, self.goal_5x5, True
        )

    def test_one_vertical_move_5x5(self):
        start = (
            1, 2, 3, 4, 5,
            16, 17, 0, 19, 6,
            15, 24, 18, 20, 7,
            14, 23, 22, 21, 8,
            13, 12, 11, 10, 9,
        )
        self.check_solvable(start, self.goal_5x5, True)

    def test_swapped_tiles_5x5(self):
        start = (
            2, 1, 3, 4, 5,
            16, 17, 18, 19, 6,
            15, 24, 0, 20, 7,
            14, 23, 22, 21, 8,
            13, 12, 11, 10, 9,
        )
        self.check_solvable(start, self.goal_5x5, False)

    # -------------------------
    # 6x6 tests (even-sized)
    # -------------------------

    def test_already_solved_6x6(self):
        self.check_solvable(
            self.goal_6x6, self.goal_6x6, True
        )

    def test_one_vertical_move_6x6(self):
        start = (
            1, 2, 3, 4, 5, 6,
            20, 21, 22, 23, 24, 7,
            19, 32, 0, 34, 25, 8,
            18, 31, 33, 35, 26, 9,
            17, 30, 29, 28, 27, 10,
            16, 15, 14, 13, 12, 11,
        )
        self.check_solvable(start, self.goal_6x6, True)

    def test_swapped_tiles_6x6(self):
        start = (
            2, 1, 3, 4, 5, 6,
            20, 21, 22, 23, 24, 7,
            19, 32, 33, 34, 25, 8,
            18, 31, 0, 35, 26, 9,
            17, 30, 29, 28, 27, 10,
            16, 15, 14, 13, 12, 11,
        )
        self.check_solvable(start, self.goal_6x6, False)

if __name__ == "__main__":
    unittest.main()
