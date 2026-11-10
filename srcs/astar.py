from heapq import heappush, heapify
from dataclasses import dataclass
from srcs.open_set import OpenSet, field
from srcs.heuristics.basic_heuristic import HeuristicFunction


@dataclass
class AStar:
    start: tuple[int]
    goal: tuple[int]
    heuristic: HeuristicFunction
    size: int

    open_set: OpenSet = field(init=False)
    closed_set: set[tuple[int]] = field(init=False)
    maximum_states: int = field(init=False)
    g_score: dict[tuple[int], int] = field(init=False)
    h_score: dict[tuple[int], int] = field(init=False)
    came_from: dict[tuple[int], tuple[int]] = field(init=False)

    def __post_init__(self) -> None:
        self.open_set = OpenSet()
        self.closed_set = set()
        self.maximum_states = 0
        self.g_score = {self.start: 0}
        self.h_score = {self.start: self.heuristic.calculate(self.start, self.goal, self.size)}
        self.came_from = {}
        self.open_set.push(self.g_score[self.start] + self.h_score[self.start], self.h_score[self.start], self.start)

        self.duplicate_rejected = 0
        self.closed_states_skipped = 0

    def _print_output(self) -> None:
        # print 4 parameters
        # ◦ Total number of states ever selected in the "opened" set (complexity in time)
        print(f"Complexity in time: {self.maximum_states}")
        # ◦ Maximum number of states ever represented in memory at the same time
        # during the search (complexity in size)
        print(f"Complexity in size: {self.open_set.get_total_states_selected()}")
        # ◦ Number of moves required to transition from the initial state to the final state,
        # according to the search
        print(f"Number of moves: {self.g_score[self.goal]}")
        # g_score[came_from(end)]
        # ◦ The ordered sequence of states that make up the solution, according to the
        # search
        print(f"The ordered sequence of states")

        for current_state in self._reconstruct_solvable_path():
            print(f"Current State: {current_state}, f_score: g(n){self.g_score[current_state]} + h(n){self.h_score[current_state]} ")
            self.print_board(current_state)

    def _reconstruct_solvable_path(self) -> list:
        current_state = self.goal
        ordered_sequence = []
        while current_state != self.start:
            ordered_sequence.insert(0, current_state)
            current_state = self.came_from[current_state]
        return ordered_sequence

    def _get_neighbors(self, state: tuple[int]) -> list[tuple[int]]:
        """
        Generate all neighboring states by moving the empty tile (0).

        A tile can move only up, down, left, or right.
        A move is valid only if it stays inside the board.

        Example: 3x3 board

            Current state:        Index positions:

            0  1  2               0  1  2
            3  4  5               3  4  5
            6  7  8               6  7  8

            The empty tile (0) is at index 0 (top-left corner).

            Possible moves:

            RIGHT:                 DOWN:

            1  0  2               3  1  2
            3  4  5               0  4  5
            6  7  8               6  7  8

            UP and LEFT are invalid because they leave the board.
        """

        zero_index = state.index(0)
        zero_row = zero_index // self.size
        zero_col = zero_index % self.size

        neighbors = []
        directions = [
            (zero_row - 1, zero_col),  # Up
            (zero_row + 1, zero_col),  # Down
            (zero_row, zero_col - 1),  # Left
            (zero_row, zero_col + 1)   # Right
        ]

        for direction in directions:
            row, col = direction
            if 0 <= row < self.size and 0 <= col < self.size:
                neighbor_index = row * self.size + col
                new_state = list(state)
                new_state[zero_index], new_state[neighbor_index] = new_state[neighbor_index], new_state[zero_index]
                neighbors.append(tuple(new_state))
        return neighbors
    
    def _get_inversions_count(self, state: tuple[int]) -> int:
        """
        Get inversions count.
        we must exclude 0 when counting the number of inversions
        """
        
        count = 0
        for i in range(len(state)):
            if state[i] == 0:
                continue
            for j in range(i + 1, len(state)):
                if state[j] == 0:
                    continue
                if state[i] > state[j]:
                    count += 1
        return count
    
    def _get_invariant(self, state: tuple[int]) -> int:
        """
        Get invariant in state
        invariant is a property that remains unchanged during legal moves.

        For odd-sized puzzles (ex: 3*3 5*5):
            invariant = inversions % 2
        
        For even-sized puzzles (ex: 4*4 6*6):
            invariant = (inversions + zero_row) % 2

        Returns:
            0 if invariant is even, 1 if invariant is odd
        """
        inversions = self._get_inversions_count(state)

        if self.size % 2 == 0:
            zero_row = state.index(0) // self.size
            inversions += zero_row

        return inversions % 2

    def _is_solvable(self) -> bool:
        """
        Check if the puzzle is solvable to use the invariant.
        """
        return self._get_invariant(self.start) == self._get_invariant(self.goal)

    def run(self) -> None:
        if not self._is_solvable():
            print("The puzzle is not solvable.")
            return
        while self.open_set:
            _, current_state = self.open_set.pop()

            if current_state in self.closed_set:
                continue

            if current_state == self.goal:
                print(f"Goal reached! {current_state}")
                self._print_output()
                return

            self.closed_set.add(current_state)

            for neighbor in self._get_neighbors(current_state):
                neighbor_g_score = self.g_score[current_state] + 1
                if neighbor_g_score >= self.g_score.get(
                    neighbor, float("inf")
                ):
                    continue
                self.came_from[neighbor] = current_state
                self.g_score[neighbor] = neighbor_g_score
                self.h_score[neighbor] = self.heuristic.calculate(
                    neighbor,
                    self.goal,
                    self.size
                )
                self.open_set.push(
                    self.g_score[neighbor] + self.h_score[neighbor],
                    self.h_score[neighbor],
                    neighbor
                )
            self.maximum_states = max(self.maximum_states, len(self.open_set) + len(self.closed_set))
        print("Fail")

    def print_info(self) -> None:
        print(f"Starting A* algorithm from {self.start} to {self.goal} using {self.heuristic.__class__.__name__} heuristic")
        print(f"Initial open set: {self.open_set._heap}, {self.open_set.get_total_states_selected()} states")
        print(f"Initial closed set: {self.closed_set}")
        print("Start: ")
        self.print_board(self.start)
        print("Goal: ")
        self.print_board(self.goal)
        pass

    def print_board(self, state: tuple[int]) -> None:
        """Print a flat N-Puzzle tuple as a square board."""
        for row in range(self.size):
            start = row * self.size
            end = start + self.size
            if state is not None:
                print(*state[start:end])


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
