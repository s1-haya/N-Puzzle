from srcs.heuristics.manhattan_distance import ManhattanDistance
from srcs.astar import AStar


def main() -> None:
    start = (3, 2, 1, 4, 0, 8, 5, 7, 6) # The permputation even because 4
    # start = (1, 2, 3, 4, 0, 8, 7, 6, 5) # The permutation odd. because 3
    goal = (1, 2, 3, 8, 0, 4, 7, 6, 5) # The permuputation even. because The permutation parity total 4
    heuristic = ManhattanDistance()
    size = 3

    astar = AStar(start=start, goal=goal, heuristic=heuristic, size=size)
    astar.print_info()
    astar.run()

if __name__ == '__main__' :
    main()
