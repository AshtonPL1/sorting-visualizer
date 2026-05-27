"""Registry of sorting algorithms with metadata."""

from .base import Algorithm
from .bubble_sort import BubbleSort
from .counting_sort import CountingSort
from .heap_sort import HeapSort
from .insertion_sort import InsertionSort
from .merge_sort import MergeSort
from .quick_sort import QuickSort

# Registry maps algorithm names (str) to Algorithm subclasses.

ALGORITHM_REGISTRY: dict[str, type[Algorithm]] = {}
ALGORITHM_REGISTRY["bubble"] = BubbleSort
ALGORITHM_REGISTRY["insertion"] = InsertionSort
ALGORITHM_REGISTRY["merge"] = MergeSort
ALGORITHM_REGISTRY["quick"] = QuickSort
ALGORITHM_REGISTRY["heap"] = HeapSort
ALGORITHM_REGISTRY["counting"] = CountingSort


# This function will be used by the UI to get available algorithms.
def get_available_algorithms() -> list[str]:
    """Return a sorted list of registered algorithm names."""
    return sorted(ALGORITHM_REGISTRY.keys())


def get_algorithm_class(name: str) -> type[Algorithm]:
    """Return the Algorithm class for the given name.

    Raises:
        KeyError: if the algorithm is not registered.
    """
    if name not in ALGORITHM_REGISTRY:
        available = ", ".join(get_available_algorithms())
        raise KeyError(
            f"Unknown algorithm '{name}'. " f"Available: {available}"
        )
    return ALGORITHM_REGISTRY[name]
