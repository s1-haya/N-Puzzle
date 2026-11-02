from heapq import heappush, heapify
from dataclasses import dataclass
from open_set import OpenSet, field


@dataclass
class AStar:
    start: tuple[int]
    goal: tuple[int]
    # heuristic: callable

    open_set: OpenSet = field(init=False)
    closed_set: set[tuple[int]] = field(init=False)
    g_score: dict[tuple[int], int] = field(init=False)
    # h_score: dict[tuple[int], int] = field(init=False)
    came_from: dict[tuple[int], tuple[int]] = field(init=False)

    def __post_init__(self):
        self.open_set = OpenSet()
        self.closed_set = set()
        self.g_score = {self.start: 0}
        # self.h_score = {self.start: self.heuristic(self.start, self.goal)}
        self.open_set.push(0, self.start)

    def run(self) -> None:
        print(f"Starting A* algorithm from {self.start} to {self.goal} using heuristic")
        pass



def main() -> None:
    start = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    # heuristic = manhattan_distance

    astar = AStar(start=start, goal=goal)
    # astar = AStar(start=start, goal=goal, heuristic=heuristic)
    astar.run()

if __name__ == '__main__' :
    main()

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
