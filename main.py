from srcs.heuristics.manhattan_distance import ManhattanDistance
from srcs.heuristics.registry import HEURISTICS
from srcs.astar import AStar
from srcs.input_parser import parse_puzzle_file
from typing import Any
from argparse import ArgumentParser


def main(*args: Any, **kwargs: Any) -> None:
    parser = ArgumentParser(
        description="Solve N-Puzzle using A* search."
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to the puzzle input file.",
    )

    parser.add_argument(
        "-H", "--heuristic",
        choices=HEURISTICS.keys(),
        default="manhattan",
        help="Heuristic function (default: manhattan).",
    )
    try:
        args = parser.parse_args(*args, **kwargs)
        size, start = parse_puzzle_file(args.input)
        goal = (1, 2, 3, 8, 0, 4, 7, 6, 5) # The permuputation even. because The permutation parity total 4
        astar = AStar(start=start, goal=goal, heuristic=HEURISTICS[args.heuristic](), size=size)
        astar.print_info()
        astar.run()
    except Exception as e:
        print(f"{__name__}: {e}")
        raise

    # # start = (1, 2, 3, 4, 0, 8, 7, 6, 5) # The permutation odd. because 3
    # # start = (3, 2, 1, 4, 0, 8, 5, 7, 6) # The permputation even because 4
    # start = (8, 6, 7, 2, 0, 5, 3, 4, 1) # 3 * 3
    # goal = (1, 2, 3, 8, 0, 4, 7, 6, 5) # The permuputation even. because The permutation parity total 4
    # heuristic = parse_heuristic("manhattan")
    # size = 3
    # astar3 = AStar(start=start, goal=goal, heuristic=heuristic, size=size)
    # astar3.run()

    # start = (10, 12, 4, 14, 9, 8, 15, 3, 1, 0, 5, 7, 11, 13, 6, 2)
    # start = (1, 2, 3, 4, 12, 13, 14, 5, 0, 11, 15, 6, 10, 9, 8, 7)
    # goal = (1, 2, 3, 4, 12, 13, 14, 5, 11, 0, 15, 6, 10, 9, 8, 7)
    # size = 4
    # astar4 = AStar(start=start, goal=goal, heuristic=heuristic, size=size)
    # astar4.run()

if __name__ == '__main__' :
    main()
