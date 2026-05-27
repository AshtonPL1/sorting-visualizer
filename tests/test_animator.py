"""Tests for SortAnimator."""

from src.algorithms.bubble_sort import BubbleSort
from src.visualization.animator import SortAnimator


class TestSortAnimator:
    """Unit tests for the SortAnimator class."""

    def test_first_frame_is_initial_state(self) -> None:
        """First cached frame must match original array with zero stats."""
        data = [5.0, 2.0, 8.0, 1.0]
        sorter = BubbleSort()
        gen = sorter.sort(data)
        animator = SortAnimator(gen, interval=100, blit=False)
        first_frame = animator._frames[0]
        arr, highlights, stats = first_frame
        assert arr == data
        assert highlights == []
        assert stats["comparisons"] == 0
        assert stats["swaps"] == 0
        assert stats["aux_elements"] == 0
        assert stats["elapsed_time"] == 0.0
        # Don't show plot
        animator._window_closed = True
        animator.ani = None

    def test_cached_frames_are_independent(self) -> None:
        """Modifying a cached array must not affect other frames."""
        data = [3.0, 1.0, 2.0]
        sorter = BubbleSort()
        gen = sorter.sort(data)
        animator = SortAnimator(gen, interval=100, blit=False)
        # Force at least 3 frames into cache
        while len(animator._frames) < 3:
            animator._add_frame(len(animator._frames))
        # Save a copy of the second frame's array before modification
        second_frame_arr_copy = animator._frames[1][0].copy()
        # Modify the first frame's array in-place
        animator._frames[0][0][0] = 999.0
        # Second frame's array must still match the saved copy
        assert animator._frames[1][0] == second_frame_arr_copy
        animator._window_closed = True
        animator.ani = None

    def test_stops_on_stopiteration(self) -> None:
        """When generator is exhausted, animator sets finished flag."""
        data = [5.0, 2.0]
        sorter = BubbleSort()
        gen = sorter.sort(data)
        animator = SortAnimator(gen, interval=100, blit=False)
        # Exhaust the generator by asking for many frames
        for _ in range(100):
            animator._add_frame(len(animator._frames))
            if animator._anim_finished:
                break
        assert animator._anim_finished is True
        animator._window_closed = True
        animator.ani = None
