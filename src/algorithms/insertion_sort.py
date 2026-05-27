"""Insertion Sort algorithm implementation."""

import time
from collections.abc import Generator
from typing import Any

from .base import Algorithm


class InsertionSort(Algorithm):
    """Insertion Sort algorithm with step-by-step visualization."""

    def sort(
        self, data: list[float] | list[int]
    ) -> Generator[tuple[list[float], list[int], dict[str, Any]], None, None]:
        """Yield states after each insertion step (shift + place)."""
        arr = [float(x) for x in data]
        n = len(arr)
        comparisons = 0
        swaps = 0  # we count each shift as one swap
        start_time = time.perf_counter()

        # Initial state
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

        for i in range(1, n):
            key = arr[i]
            j = i - 1
            # Highlight current element being inserted
            # Move elements greater than key forward
            while j >= 0:
                comparisons += 1
                if arr[j] > key:
                    arr[j + 1] = arr[j]
                    swaps += 1
                    yield (
                        arr.copy(),
                        [
                            j + 1,
                            j,
                        ],
                        {
                            "comparisons": comparisons,
                            "swaps": swaps,
                            "aux_elements": 0,
                            "elapsed_time": (time.perf_counter() - start_time),
                        },
                    )
                    j -= 1
                else:
                    break
            # Place key
            arr[j + 1] = key
            yield (
                arr.copy(),
                [j + 1],
                {
                    "comparisons": comparisons,
                    "swaps": swaps,
                    "aux_elements": 0,
                    "elapsed_time": time.perf_counter() - start_time,
                },
            )

        # Final state (no highlights)
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
