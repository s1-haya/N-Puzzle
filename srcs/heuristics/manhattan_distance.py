from srcs.heuristics.basic_heuristic import HeuristicFunction


class ManhattanDistance(HeuristicFunction):
	"""Heuristic function that calculates the Manhattan distance for a given state."""
	
	def calculate(self, state: tuple[int, ...], goal: tuple[int, ...], size: int) -> int:
		"""
		Calculate the Manhattan distance between the current state and the goal state.
		
		The distance is calculated by summing the absolute differences
		between the current and goal positions of each tile, excluding the empty tile (0).

		ex) size = 3
		START 		GOAL
		2 1 3		1 2 3
		0 8 4		8 0 4
		5 6 7		7 6 5

		calculate the Manhattan distance
		1 1 0
		/ 1 0
		2 0 2
		
		Total distance: 7
		"""

		distance = 0
		for index, value in enumerate(state):
			if value == 0:
				continue

			goal_index = goal.index(value)
			if index == goal_index:
				continue

			curr_row = index // size
			curr_col = index % size
			goal_row = goal_index // size
			goal_col = goal_index % size
			distance += abs(goal_col - curr_col) + abs(goal_row - curr_row)

		return distance
