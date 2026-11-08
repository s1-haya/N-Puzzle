from srcs.heuristics.basic_heuristic import HeuristicFunction


class LinearConflict(HeuristicFunction):
    """Manhattan distance plus two moves per necessary row/column detour.

    For each row/column, goal-aligned tiles must appear in goal order.
    The minimum number that must leave that line is bounded below by
    len(sequence) - length_of_longest_increasing_subsequence(sequence).
    Counting these detours avoids overestimating overlapping conflicts.
    """

    @staticmethod
    def _min_tiles_to_remove(sequence: list[int]) -> int:
        """Minimum removals to make a sequence strictly increasing."""
        if not sequence:
            return 0
        lengths = [1] * len(sequence)
        for index in range(len(sequence)):
            for previous in range(index):
                if sequence[previous] < sequence[index]:
                    lengths[index] = max(lengths[index], lengths[previous] + 1)
        return len(sequence) - max(lengths)

    def calculate(
        self, state: tuple[int, ...], goal: tuple[int, ...], size: int
    ) -> int:
        """
        Return Manhattan distance plus non-overlapping conflict penalties.

        Linear Conflict = Manhattan Distance + (2 * number of linear conflicts)
        """
        manhattan = 0
        conflicts = 0


        for index, tile in enumerate(state):
            if tile == 0:
                continue
            goal_index = goal.index(tile)
            
            if index == goal_index:
                continue
            curr_row = index // size
            curr_col = index % size
            goal_row = goal_index // size
            goal_col = goal_index % size
            manhattan += abs(goal_col - curr_col) + abs(goal_row - curr_row)

        for row in range(size):
            goal_columns = []
            for col in range(size):
                tile = state[row * size + col]
                if tile and goal.index(tile) // size == row:
                    goal_columns.append(goal.index(tile) % size)
            conflicts += self._min_tiles_to_remove(goal_columns)

        for col in range(size):
            goal_rows = []
            for row in range(size):
                tile = state[row * size + col]
                if tile and goal.index(tile) % size == col:
                    goal_rows.append(goal.index(tile) // size)
            conflicts += self._min_tiles_to_remove(goal_rows)

        return manhattan + 2 * conflicts
