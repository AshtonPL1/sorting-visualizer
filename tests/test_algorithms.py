"""Tests for all sorting algorithms."""

import pytest

from src.algorithms.base import AlgorithmIncompatibleError
from src.algorithms.bubble_sort import BubbleSort
from src.algorithms.counting_sort import CountingSort
from src.algorithms.heap_sort import HeapSort
from src.algorithms.insertion_sort import InsertionSort
from src.algorithms.merge_sort import MergeSort
from src.algorithms.quick_sort import QuickSort


class TestBubbleSort:
    """Unit tests for Bubble Sort."""

    def test_initial_frame(self) -> None:
        """First frame must be original array with zero stats."""
        sorter = BubbleSort()
        data = [5.0, 2.0, 9.0, 1.0]
        gen = sorter.sort(data)
        arr, highlights, stats = next(gen)
        assert arr == [5.0, 2.0, 9.0, 1.0]
        assert highlights == []
        assert stats["comparisons"] == 0
        assert stats["swaps"] == 0
        assert stats["aux_elements"] == 0
        assert stats["elapsed_time"] == 0.0

    def test_sorts_correctly(self) -> None:
        """After exhausting generator, array must be sorted."""
        sorter = BubbleSort()
        data = [4.0, 3.0, 2.0, 1.0]
        gen = sorter.sort(data)
        last_arr = None
        for frame in gen:
            last_arr = frame[0]
        assert last_arr == [1.0, 2.0, 3.0, 4.0]

    def test_frames_independent(self) -> None:
        """Each yielded array must be a different copy."""
        sorter = BubbleSort()
        data = [3.0, 1.0, 2.0]
        gen = sorter.sort(data)
        frames = list(gen)
        for i in range(len(frames) - 1):
            prev_arr = frames[i][0].copy()
            frames[i][0][0] = 999.0
            assert frames[i][0] != prev_arr
            assert frames[i + 1][0][0] != 999.0

    def test_empty_array(self) -> None:
        sorter = BubbleSort()
        gen = sorter.sort([])
        frames = list(gen)
        assert len(frames) >= 1
        init_arr, init_hl, init_st = frames[0]
        assert init_arr == []
        assert init_hl == []
        assert init_st["comparisons"] == 0
        assert init_st["swaps"] == 0
        assert init_st["aux_elements"] == 0
        for arr, _, _ in frames[1:]:
            assert arr == []

    def test_single_element(self) -> None:
        sorter = BubbleSort()
        gen = sorter.sort([42.0])
        frames = list(gen)
        assert len(frames) >= 1
        init_arr, _, init_st = frames[0]
        assert init_arr == [42.0]
        assert init_st["comparisons"] == 0
        assert init_st["swaps"] == 0
        for arr, _, _ in frames[1:]:
            assert arr == [42.0]


class TestCountingSort:
    """Unit tests for Counting Sort."""

    def test_compatibility_positive_ints(self) -> None:
        """Should accept non-negative integers."""
        CountingSort.check_compatibility([0, 5, 2, 9])

    def test_compatibility_rejects_floats(self) -> None:
        """Floats are not allowed."""
        with pytest.raises(AlgorithmIncompatibleError):
            CountingSort.check_compatibility([1.0, 2.0])

    def test_compatibility_rejects_negative(self) -> None:
        with pytest.raises(AlgorithmIncompatibleError):
            CountingSort.check_compatibility([1, -2, 3])

    def test_sorts_integers(self) -> None:
        sorter = CountingSort()
        data = [4, 2, 2, 8, 3, 3, 1]
        gen = sorter.sort(data)
        frames = list(gen)
        last_arr = frames[-1][0]
        assert last_arr == [1, 2, 2, 3, 3, 4, 8]

    def test_empty_array(self) -> None:
        sorter = CountingSort()
        gen = sorter.sort([])
        frames = list(gen)
        assert len(frames) == 1
        assert frames[0][0] == []

    def test_single_element(self) -> None:
        sorter = CountingSort()
        gen = sorter.sort([7])
        frames = list(gen)
        assert frames[0][0] == [7]
        assert frames[-1][0] == [7]

    def test_highlights_single_index(self) -> None:
        """Each placement frame should highlight exactly one index."""
        sorter = CountingSort()
        data = [3, 1, 2]
        gen = sorter.sort(data)
        frames = list(gen)
        placement_frames = [f for f in frames if f[1] != []]
        assert len(placement_frames) == len(data)
        for _arr, hl, st in placement_frames:
            assert len(hl) == 1
            assert st["aux_elements"] > 0


class TestInsertionSort:
    """Unit tests for Insertion Sort."""

    def test_initial_frame(self) -> None:
        sorter = InsertionSort()
        data = [5.0, 2.0, 9.0, 1.0]
        gen = sorter.sort(data)
        arr, highlights, stats = next(gen)
        assert arr == [5.0, 2.0, 9.0, 1.0]
        assert highlights == []
        assert stats["comparisons"] == 0
        assert stats["swaps"] == 0
        assert stats["aux_elements"] == 0
        assert stats["elapsed_time"] == 0.0

    def test_sorts_correctly(self) -> None:
        sorter = InsertionSort()
        data = [4.0, 3.0, 2.0, 1.0]
        gen = sorter.sort(data)
        last_arr = None
        for frame in gen:
            last_arr = frame[0]
        assert last_arr == [1.0, 2.0, 3.0, 4.0]

    def test_frames_independent(self) -> None:
        sorter = InsertionSort()
        data = [3.0, 1.0, 2.0]
        gen = sorter.sort(data)
        frames = list(gen)
        for i in range(len(frames) - 1):
            prev_arr = frames[i][0].copy()
            frames[i][0][0] = 999.0
            assert frames[i][0] != prev_arr
            assert frames[i + 1][0][0] != 999.0

    def test_empty_array(self) -> None:
        sorter = InsertionSort()
        gen = sorter.sort([])
        frames = list(gen)
        assert len(frames) >= 1
        assert frames[0][0] == []

    def test_single_element(self) -> None:
        sorter = InsertionSort()
        gen = sorter.sort([42.0])
        frames = list(gen)
        assert len(frames) >= 1
        assert frames[0][0] == [42.0]
        for arr, _, _ in frames[1:]:
            assert arr == [42.0]


class TestMergeSort:
    """Unit tests for Merge Sort (iterative bottom-up)."""

    def test_initial_frame(self) -> None:
        sorter = MergeSort()
        data = [5.0, 2.0, 9.0, 1.0]
        gen = sorter.sort(data)
        arr, highlights, stats = next(gen)
        assert arr == [5.0, 2.0, 9.0, 1.0]
        assert highlights == []
        assert stats["comparisons"] == 0
        assert stats["swaps"] == 0
        assert stats["aux_elements"] == 0
        assert stats["elapsed_time"] == 0.0

    def test_sorts_correctly(self) -> None:
        sorter = MergeSort()
        data = [4.0, 3.0, 2.0, 1.0]
        gen = sorter.sort(data)
        last_arr = None
        for frame in gen:
            last_arr = frame[0]
        assert last_arr == [1.0, 2.0, 3.0, 4.0]

    def test_frames_independent(self) -> None:
        sorter = MergeSort()
        data = [3.0, 1.0, 2.0]
        gen = sorter.sort(data)
        frames = list(gen)
        for i in range(len(frames) - 1):
            prev_arr = frames[i][0].copy()
            frames[i][0][0] = 999.0
            assert frames[i][0] != prev_arr
            assert frames[i + 1][0][0] != 999.0

    def test_empty_array(self) -> None:
        sorter = MergeSort()
        gen = sorter.sort([])
        frames = list(gen)
        assert len(frames) >= 1
        assert frames[0][0] == []

    def test_single_element(self) -> None:
        sorter = MergeSort()
        gen = sorter.sort([42.0])
        frames = list(gen)
        assert len(frames) >= 1
        assert frames[0][0] == [42.0]
        for arr, _, _ in frames[1:]:
            assert arr == [42.0]

    def test_aux_elements_during_merge(self) -> None:
        """During merge steps, aux_elements should equal len(array)."""
        sorter = MergeSort()
        data = [3.0, 2.0, 1.0]
        gen = sorter.sort(data)
        frames = list(gen)
        merge_frames = [f for f in frames if f[2]["aux_elements"] > 0]
        assert len(merge_frames) > 0
        for _, hl, st in merge_frames:
            assert len(hl) == 1
            assert st["aux_elements"] == len(data)


class TestQuickSort:
    """Unit tests for Quick Sort (iterative, 3-way)."""

    def test_initial_frame(self) -> None:
        sorter = QuickSort()
        data = [5.0, 2.0, 9.0, 1.0]
        gen = sorter.sort(data)
        arr, highlights, stats = next(gen)
        assert arr == [5.0, 2.0, 9.0, 1.0]
        assert highlights == []
        assert stats["comparisons"] == 0
        assert stats["swaps"] == 0
        assert stats["aux_elements"] == 0
        assert stats["elapsed_time"] == 0.0

    def test_sorts_correctly(self) -> None:
        sorter = QuickSort()
        data = [4.0, 3.0, 2.0, 1.0]
        gen = sorter.sort(data)
        last_arr = None
        for frame in gen:
            last_arr = frame[0]
        assert last_arr == [1.0, 2.0, 3.0, 4.0]

    def test_frames_independent(self) -> None:
        sorter = QuickSort()
        data = [3.0, 1.0, 2.0]
        gen = sorter.sort(data)
        frames = list(gen)
        for i in range(len(frames) - 1):
            prev_arr = frames[i][0].copy()
            frames[i][0][0] = 999.0
            assert frames[i][0] != prev_arr
            assert frames[i + 1][0][0] != 999.0

    def test_empty_array(self) -> None:
        sorter = QuickSort()
        gen = sorter.sort([])
        frames = list(gen)
        assert len(frames) >= 1
        assert frames[0][0] == []

    def test_single_element(self) -> None:
        sorter = QuickSort()
        gen = sorter.sort([42.0])
        frames = list(gen)
        assert len(frames) >= 1
        assert frames[0][0] == [42.0]
        for arr, _, _ in frames[1:]:
            assert arr == [42.0]

    def test_has_pivot_highlight(self) -> None:
        """At least one frame should highlight a single index (pivot)."""
        sorter = QuickSort()
        data = [3.0, 2.0, 1.0]
        gen = sorter.sort(data)
        frames = list(gen)
        single_highlights = [f for f in frames if len(f[1]) == 1]
        assert len(single_highlights) > 0


class TestHeapSort:
    """Unit tests for Heap Sort (iterative, in-place)."""

    def test_initial_frame(self) -> None:
        sorter = HeapSort()
        data = [5.0, 2.0, 9.0, 1.0]
        gen = sorter.sort(data)
        arr, highlights, stats = next(gen)
        assert arr == [5.0, 2.0, 9.0, 1.0]
        assert highlights == []
        assert stats["comparisons"] == 0
        assert stats["swaps"] == 0
        assert stats["aux_elements"] == 0
        assert stats["elapsed_time"] == 0.0

    def test_sorts_correctly(self) -> None:
        sorter = HeapSort()
        data = [4.0, 3.0, 2.0, 1.0]
        gen = sorter.sort(data)
        last_arr = None
        for frame in gen:
            last_arr = frame[0]
        assert last_arr == [1.0, 2.0, 3.0, 4.0]

    def test_frames_independent(self) -> None:
        sorter = HeapSort()
        data = [3.0, 1.0, 2.0]
        gen = sorter.sort(data)
        frames = list(gen)
        for i in range(len(frames) - 1):
            prev_arr = frames[i][0].copy()
            frames[i][0][0] = 999.0
            assert frames[i][0] != prev_arr
            assert frames[i + 1][0][0] != 999.0

    def test_empty_array(self) -> None:
        sorter = HeapSort()
        gen = sorter.sort([])
        frames = list(gen)
        assert len(frames) >= 1
        assert frames[0][0] == []

    def test_single_element(self) -> None:
        sorter = HeapSort()
        gen = sorter.sort([42.0])
        frames = list(gen)
        assert len(frames) >= 1
        assert frames[0][0] == [42.0]
        for arr, _, _ in frames[1:]:
            assert arr == [42.0]

    def test_swaps_present(self) -> None:
        """Heap Sort involves swaps; ensure some frames have swaps > 0."""
        sorter = HeapSort()
        data = [3.0, 1.0, 2.0]
        gen = sorter.sort(data)
        frames = list(gen)
        swap_frames = [f for f in frames if f[2]["swaps"] > 0]
        assert len(swap_frames) > 0
