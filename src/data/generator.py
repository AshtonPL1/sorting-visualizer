"""Utilities for generating test data arrays."""

import random


def generate_random_array(
    size: int, min_val: float = 0.0, max_val: float = 100.0
) -> list[float]:
    """Return a list of random floats."""
    return [random.uniform(min_val, max_val) for _ in range(size)]
