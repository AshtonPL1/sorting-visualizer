"""Merge Sort algorithm (iterative bottom-up)."""

import time
from collections.abc import Generator
from typing import Any

from .base import Algorithm


class MergeSort(Algorithm):
    """Iterative bottom-up Merge Sort with step-by-step visualization."""

    def sort(
        self, data: list[float] | list[int]
    ) -> Generator[tuple[list[float], list[int], dict[str, Any]], None, None]:
        """Yield states during merging operations."""
        arr = [float(x) for x in data]
        n = len(arr)
        comparisons = 0
        swaps = 0
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

        width = 1
        while width < n:
            for left_start in range(0, n, 2 * width):
                mid = min(left_start + width, n)
                right_end = min(left_start + 2 * width, n)

                left = arr[left_start:mid]
                right = arr[mid:right_end]

                i = j = 0
                k = left_start

                while i < len(left) and j < len(right):
                    comparisons += 1
                    if left[i] <= right[j]:
                        arr[k] = left[i]
                        i += 1
                    else:
                        arr[k] = right[j]
                        j += 1
                    swaps += 1
                    yield (
                        arr.copy(),
                        [k],
                        {
                            "comparisons": comparisons,
                            "swaps": swaps,
                            "aux_elements": n,
                            "elapsed_time": (time.perf_counter() - start_time),
                        },
                    )
                    k += 1

                while i < len(left):
                    arr[k] = left[i]
                    i += 1
                    swaps += 1
                    yield (
                        arr.copy(),
                        [k],
                        {
                            "comparisons": comparisons,
                            "swaps": swaps,
                            "aux_elements": n,
                            "elapsed_time": (time.perf_counter() - start_time),
                        },
                    )
                    k += 1

                while j < len(right):
                    arr[k] = right[j]
                    j += 1
                    swaps += 1
                    yield (
                        arr.copy(),
                        [k],
                        {
                            "comparisons": comparisons,
                            "swaps": swaps,
                            "aux_elements": n,
                            "elapsed_time": (time.perf_counter() - start_time),
                        },
                    )
                    k += 1

            width *= 2

        # Final state
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
