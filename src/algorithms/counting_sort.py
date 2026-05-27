"""Counting Sort algorithm (non-negative integers only)."""

import time
from collections.abc import Generator
from typing import Any

from .base import Algorithm, AlgorithmIncompatibleError


class CountingSort(Algorithm):
    """Counting Sort for non-negative integers only."""

    @staticmethod
    def check_compatibility(data: list[Any]) -> None:
        """Raise AlgorithmIncompatibleError if data invalid."""
        for x in data:
            if not isinstance(x, int) or x < 0:
                raise AlgorithmIncompatibleError(
                    "Counting Sort requires non-negative integers only."
                )

    def sort(
        self, data: list[int]  # type: ignore[override]
    ) -> Generator[tuple[list[int], list[int], dict[str, Any]], None, None]:
        """Yield states: counting, then placing each element."""
        arr = data.copy()
        n = len(arr)
        if n == 0:
            yield (
                [],
                [],
                {
                    "comparisons": 0,
                    "swaps": 0,
                    "aux_elements": 0,
                    "elapsed_time": 0.0,
                },
            )
            return

        max_val = max(arr)
        start_time = time.perf_counter()

        # Initial state (before any allocation)
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

        # Keep original array for reading values during placement
        original = arr.copy()

        # Allocate count array and output array
        counts = [0] * (max_val + 1)
        output = [0] * n
        total_aux = len(counts) + len(output)

        # Count frequencies
        for val in original:
            counts[val] += 1

        # Cumulative counts
        for i in range(1, len(counts)):
            counts[i] += counts[i - 1]

        comparisons = 0
        swaps = 0

        # Place elements using original values (read from 'original')
        for i in range(n - 1, -1, -1):
            val = original[i]
            pos = counts[val] - 1
            counts[val] -= 1
            output[pos] = val
            swaps += 1
            # Show current state of output (partially filled)
            arr = output.copy()
            yield (
                arr.copy(),
                [pos],  # highlight the placed index
                {
                    "comparisons": comparisons,
                    "swaps": swaps,
                    "aux_elements": total_aux,
                    "elapsed_time": time.perf_counter() - start_time,
                },
            )

        # Final state (no highlights, aux_elements back to 0)
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
