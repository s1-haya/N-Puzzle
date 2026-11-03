from dataclasses import dataclass, field
from abc import ABC, abstractmethod


@dataclass
class HeuristicFunction(ABC):
	"""Abstract base class for heuristic functions."""

	@abstractmethod
	def calculate(self, state: tuple[int, ...], goal: tuple[int, ...]) -> int:
		"""Calculate the heuristic value for a given state."""
		pass

