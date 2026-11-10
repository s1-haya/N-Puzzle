from srcs.heuristics.manhattan_distance import ManhattanDistance
from srcs.heuristics.misplaced_tiles import MisplacedTiles
from srcs.heuristics.linear_conflict import LinearConflict


HEURISTICS: dict[str, type[HeuristicFunction]] = {
    "manhattan": ManhattanDistance,
    "misplaced": MisplacedTiles,
    "linear_conflict": LinearConflict,
}
