"""Simple demo to test Bubble Sort visualization."""

from src.algorithms.bubble_sort import BubbleSort
from src.data.generator import generate_random_array
from src.visualization.animator import SortAnimator

# Generate a small random array
array = generate_random_array(20, min_val=1.0, max_val=50.0)

# Create Bubble Sort generator
sorter = BubbleSort()
gen = sorter.sort(array)

# Create animator and start
animator = SortAnimator(gen, interval=100, blit=False)
animator.start()
