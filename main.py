from srcs.heuristics.manhattan_distance import ManhattanDistance
from srcs.heuristics.registry import HEURISTICS
from srcs.astar import AStar
from srcs.input_parser import parse_puzzle_file
from typing import Any
from argparse import ArgumentParser
from srcs.generate_snail_goal import generate_snail_goal


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
        goal = generate_snail_goal(size)
        astar = AStar(start=start, goal=goal, heuristic=HEURISTICS[args.heuristic](), size=size)
        astar.print_info()
        astar.run()
    except Exception as e:
        print(f"{__name__}: {e}")
        raise

if __name__ == '__main__' :
    main()
