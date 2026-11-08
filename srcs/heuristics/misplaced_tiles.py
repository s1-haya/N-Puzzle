from srcs.heuristics.basic_heuristic import HeuristicFunction


class MisplacedTiles(HeuristicFunction):
    """Count numbered tiles that are not in their goal positions."""

    def calculate(
        self, state: tuple[int, ...], goal: tuple[int, ...], size: int
    ) -> int:
        """Return the number of misplaced numbered tiles (ignore 0)."""
        return sum(
            tile != 0 and tile != goal[position]
            for position, tile in enumerate(state)
        )
