import heapq
from itertools import count
from dataclasses import dataclass, field


@dataclass
class OpenSet:
    """A min-heap data structure to manage the open set of states in the A*"""
    _heap: list[tuple[int, tuple[int, ...]]] = field(init=False, default_factory=list)
    counter: int = field(init=False, default_factory=count().__next__)

    def push(self, f_cost: int, state: tuple[int, ...]) -> None:
        """Push a new board state into the openset with its f cost."""
        next(self.counter)
        heapq.heappush(
            self._heap,
            (f_cost, state)
        )

    def pop(self) -> tuple[int, tuple[int, ...]]:
        """Pop the board state with the lowest f cost from the openset."""
        f_cost, state = heapq.heappop(self._heap)
        return f_cost, state

    def __len__(self) -> int:
        """Return the number of states in the openset."""
        return len(self._heap)

    def get_total_count(self) -> int:
        """Return the total number of states added to the openset."""
        return self.counter
