"""Bubble Sort algorithm implementation."""

import time
from collections.abc import Generator
from typing import Any

from .base import Algorithm


class BubbleSort(Algorithm):
    """Bubble Sort algorithm with step-by-step visualization."""

    def sort(
        self, data: list[float] | list[int]
    ) -> Generator[tuple[list[float], list[int], dict[str, Any]], None, None]:
        """Yield each state of the array after every swap."""
        arr = [float(x) for x in data]
        n = len(arr)
        comparisons = 0
        swaps = 0
        start_time = time.perf_counter()

        # Initial state (before any operations)
        yield (
            arr.copy(),
            [],
            {
                "comparisons": 0,
                "swaps": 0,
                "aux_elements": 0,
                "elapsed_time": 0.0,
            },
        )

        for i in range(n - 1):
            swapped = False
            for j in range(n - 1 - i):
                comparisons += 1
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swaps += 1
                    swapped = True
                    # Yield after swap, highlighting swapped indices
                    yield (
                        arr.copy(),
                        [j, j + 1],
                        {
                            "comparisons": comparisons,
                            "swaps": swaps,
                            "aux_elements": 0,
                            "elapsed_time": (time.perf_counter() - start_time),
                        },
                    )
            if not swapped:
                break  # early exit if sorted

        # Final state: no highlights, just ensure last frame is yielded
        yield (
            arr.copy(),
            [],
            {
                "comparisons": comparisons,
                "swaps": swaps,
                "aux_elements": 0,
                "elapsed_time": time.perf_counter() - start_time,
            },
        )
