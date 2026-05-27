"""Base class and exceptions for sorting algorithms."""

from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import Any


class AlgorithmIncompatibleError(Exception):
    """Raised when data is incompatible with a given algorithm."""


class SortingError(Exception):
    """Raised when the final sorted array is not actually sorted."""


class Algorithm(ABC):
    """Abstract base class for all sorting algorithms."""

    @abstractmethod
    def sort(
        self,
        data: list[float] | list[int],
    ) -> Generator[tuple[list[Any], list[int], dict[str, Any]], None, None]:
        """
        Generator that yields (array_copy, highlights, stats) tuples.

        Yields:
            tuple: (array, highlights, stats) where
                array is a copy of the current state,
                highlights is a list of indices to highlight,
                stats is a dict with keys comparisons, swaps,
                aux_elements, elapsed_time.
        """
        ...
