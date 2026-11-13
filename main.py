from srcs.heuristics.manhattan_distance import ManhattanDistance
from srcs.heuristics.registry import HEURISTICS
from srcs.astar import AStar
from srcs.input_parser import parse_argument, parse_puzzle_file
from typing import Any
from argparse import ArgumentParser
from srcs.generate_snail_goal import generate_snail_goal


def main(*args: Any, **kwargs: Any) -> None:
    try:
        args = parse_argument(*args, **kwargs)
        size, start = parse_puzzle_file(args.input)
        goal = generate_snail_goal(size)
        astar = AStar(start=start, goal=goal, heuristic=HEURISTICS[args.heuristic](), size=size)
        astar.run()
    except Exception as e:
        print(f"{__name__}: {e}")
        raise

if __name__ == '__main__' :
    main()
