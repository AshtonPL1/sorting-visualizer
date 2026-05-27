"""Quick Sort algorithm (iterative, 3-way partition, median-of-three)."""

import time
from collections.abc import Generator
from typing import Any

from .base import Algorithm


class QuickSort(Algorithm):
    """Iterative Quick Sort with 3-way partitioning and median pivot."""

    def sort(
        self, data: list[float] | list[int]
    ) -> Generator[tuple[list[float], list[int], dict[str, Any]], None, None]:
        """Yield states: pivot selection, swaps, final."""
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

        # Stack stores (low, high) intervals to process
        stack: list[tuple[int, int]] = [(0, n - 1)]

        while stack:
            low, high = stack.pop()
            aux_elements = len(stack)  # current stack depth

            if low >= high:
                continue

            # --- Pivot selection (median-of-three) ---
            mid = (low + high) // 2
            # Order low, mid, high
            if arr[low] > arr[mid]:
                arr[low], arr[mid] = arr[mid], arr[low]
                swaps += 1
            if arr[low] > arr[high]:
                arr[low], arr[high] = arr[high], arr[low]
                swaps += 1
            if arr[mid] > arr[high]:
                arr[mid], arr[high] = arr[high], arr[mid]
                swaps += 1
            # Place median at arr[low] and use as pivot
            arr[low], arr[mid] = arr[mid], arr[low]
            swaps += 1
            pivot = arr[low]

            # Yield pivot selection frame (highlight pivot position)
            yield (
                arr.copy(),
                [low],  # pivot is now at index low
                {
                    "comparisons": comparisons,
                    "swaps": swaps,
                    "aux_elements": aux_elements,
                    "elapsed_time": time.perf_counter() - start_time,
                },
            )

            # 3-way partition
            lt = low
            gt = high
            i = low + 1
            while i <= gt:
                comparisons += 1
                if arr[i] < pivot:
                    arr[lt], arr[i] = arr[i], arr[lt]
                    swaps += 1
                    yield (
                        arr.copy(),
                        [lt, i],
                        {
                            "comparisons": comparisons,
                            "swaps": swaps,
                            "aux_elements": aux_elements,
                            "elapsed_time": (time.perf_counter() - start_time),
                        },
                    )
                    lt += 1
                    i += 1
                elif arr[i] > pivot:
                    arr[i], arr[gt] = arr[gt], arr[i]
                    swaps += 1
                    yield (
                        arr.copy(),
                        [i, gt],
                        {
                            "comparisons": comparisons,
                            "swaps": swaps,
                            "aux_elements": aux_elements,
                            "elapsed_time": (time.perf_counter() - start_time),
                        },
                    )
                    gt -= 1
                else:
                    i += 1

            # Push subproblems (larger first for stack efficiency)
            if low < lt - 1:
                stack.append((low, lt - 1))
            if gt + 1 < high:
                stack.append((gt + 1, high))

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
