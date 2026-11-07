import heapq
from itertools import count
from typing import Iterator
from dataclasses import dataclass, field


@dataclass
class OpenSet:
    """A min-heap data structure to manage the open set of states in the A*"""
    _heap: list[tuple[int, tuple[int, ...]]] = field(init=False, default_factory=list)
    _order: Iterator[int] = field(init=False, default_factory=count)
    states_selected: int = field(init=False, default=0)

    def push(self, f_score: int, h_score: int, state: tuple[int, ...]) -> None:
        """
        Add a state to the open set.

        States are prioritized by:
        1. Lowest f-score (g + h).
        2. Lowest h-score if f-scores are equal.
        3. Insertion order if both scores are equal.
        """
        heapq.heappush(
            self._heap,
            (f_score, h_score, next(self._order), state)
        )

    def pop(self) -> tuple[int, tuple[int, ...]]:
        """
        Remove and return the highest-priority state.

        Returns:
            A tuple containing the f-score and board state.
        """
        f_score, _, _, state = heapq.heappop(self._heap)
        self.states_selected += 1
        return f_score, state

    def __len__(self) -> int:
        """Return the number of states in the openset."""
        return len(self._heap)

    def get_total_states_selected(self) -> int:
        """Return the total number of states added to the openset."""
        return self.states_selected
