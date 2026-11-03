from heapq import heappush, heapify
from dataclasses import dataclass
from srcs.open_set import OpenSet, field
from srcs.heuristics.basic_heuristic import HeuristicFunction


@dataclass
class AStar:
    start: tuple[int]
    goal: tuple[int]
    heuristic: HeuristicFunction

    open_set: OpenSet = field(init=False)
    closed_set: set[tuple[int]] = field(init=False)
    g_score: dict[tuple[int], int] = field(init=False)
    # h_score: dict[tuple[int], int] = field(init=False)
    came_from: dict[tuple[int], tuple[int]] = field(init=False)

    def __post_init__(self):
        self.open_set = OpenSet()
        self.open_set.push(0, self.start)
        self.closed_set = set()
        self.g_score = {self.start: 0}
        # self.h_score = {self.start: self.heuristic(self.start, self.goal)}

    def run(self) -> None:
        pass

    def print_info(self) -> None:
        print(f"Starting A* algorithm from {self.start} to {self.goal} using {self.heuristic.__class__.__name__} heuristic")
        print(f"Initial open set: {self.open_set._heap}, {self.open_set.get_total_count()} states")
        print(f"Initial closed set: {self.closed_set}")
        pass



# # T: Goal State
# # C: Current State
# # S: Start State

# ---

# # f(n) = g(n) + h(n)
# # n: node
# # f: total cost
# # g: real cost from S to C
# # h: estimate cost from C to G

# ---
# # Heuristic Function
# -> to estiate the cost to move from C to G

# A* -> 500
# - H1
# - H2
# - H3


# def manhattan_distance()
#     p, q
#     p(x1, y1), q(x2, y2)
#     |x1 - x2| + |y1 - y2|
#     list[[1, 2], [2, 1]]
