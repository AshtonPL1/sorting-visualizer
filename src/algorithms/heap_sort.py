"""Heap Sort algorithm (iterative, in-place)."""

import time
from collections.abc import Generator
from typing import Any

from .base import Algorithm


class HeapSort(Algorithm):
    """Heap Sort with step-by-step visualization of heapify and extraction."""

    def sort(
        self, data: list[float] | list[int]
    ) -> Generator[tuple[list[float], list[int], dict[str, Any]], None, None]:
        """Yield states during heap construction and sorting."""
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

        def _sift_down(i: int, heap_size: int) -> Generator[Any, None, None]:
            """Sift down the element at index i within heap of given size."""
            nonlocal comparisons, swaps
            while True:
                largest = i
                left = 2 * i + 1
                right = 2 * i + 2

                if left < heap_size:
                    comparisons += 1
                    if arr[left] > arr[largest]:
                        largest = left
                if right < heap_size:
                    comparisons += 1
                    if arr[right] > arr[largest]:
                        largest = right

                if largest != i:
                    arr[i], arr[largest] = arr[largest], arr[i]
                    swaps += 1
                    # Yield after swap, highlighting swapped indices
                    yield (
                        arr.copy(),
                        [i, largest],
                        {
                            "comparisons": comparisons,
                            "swaps": swaps,
                            "aux_elements": 0,
                            "elapsed_time": (time.perf_counter() - start_time),
                        },
                    )
                    i = largest
                else:
                    break

        # Build max heap (bottom-up)
        for start in range(n // 2 - 1, -1, -1):
            yield from _sift_down(start, n)

        # Extract elements one by one
        for end in range(n - 1, 0, -1):
            arr[0], arr[end] = arr[end], arr[0]
            swaps += 1
            # Yield swap of root and last element
            yield (
                arr.copy(),
                [0, end],
                {
                    "comparisons": comparisons,
                    "swaps": swaps,
                    "aux_elements": 0,
                    "elapsed_time": time.perf_counter() - start_time,
                },
            )
            # Restore heap property on reduced heap
            yield from _sift_down(0, end)

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
