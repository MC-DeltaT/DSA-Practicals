from typing import Callable, MutableSequence, Tuple

import numpy


__all__ = [
    "bubble_sort",
    "counting_sort",
    "insertion_sort",
    "mergesort",
    "quicksort_3w",
    "quicksort_bad",
    "quicksort_mo3",
    "radix_sort_lsd",
    "selection_sort",
    "shell_sort"
]


def bubble_sort(seq: MutableSequence):
    n = 0
    is_sorted = False
    while not is_sorted and n < len(seq) - 1:
        is_sorted = True
        for i in range(len(seq) - 1 - n):
            if seq[i] > seq[i + 1]:
                seq[i], seq[i + 1] = seq[i + 1], seq[i]
                is_sorted = False
        n += 1


def insertion_sort(seq):
    for n in range(1, len(seq)):
        i = n
        while seq[i - 1] > seq[i] and i > 0:
            seq[i], seq[i - 1] = seq[i - 1], seq[i]
            i -= 1


def selection_sort(seq):
    for i in range(len(seq)):
        min_idx = i
        for j in range(i + 1, len(seq)):
            if seq[j] < seq[min_idx]:
                min_idx = j
        seq[i], seq[min_idx] = seq[min_idx], seq[i]


# Sorts seq in place using the mergesort algorithm.
def mergesort(seq: MutableSequence) -> None:
    # Sorts seq on the range [left, right].
    def _mergesort(seq: MutableSequence, left: int, right: int):
        if left < right:
            middle = (left + right) // 2
            _mergesort(seq, left, middle)
            _mergesort(seq, middle + 1, right)
            _merge(seq, left, middle + 1, right + 1)

    # Merges seq[left:middle] and seq[middle:right] into seq[left:right]
    def _merge(seq: MutableSequence, left: int, middle: int, right: int):
        tmp = numpy.empty(right - left, dtype=object)
        i = left
        j = middle
        k = 0
        while i < middle and j < right:
            # Using <= for stable sort.
            if seq[i] <= seq[j]:
                tmp[k] = seq[i]
                i += 1
            else:
                tmp[k] = seq[j]
                j += 1
            k += 1

        for i in range(i, middle):
            tmp[k] = seq[i]
            k += 1
        for j in range(j, right):
            tmp[k] = seq[j]
            k += 1

        for k, e in zip(range(left, right), tmp):
            seq[k] = e

    _mergesort(seq, 0, len(seq) - 1)


# Pivots on the leftmost element.
def quicksort_bad(seq: MutableSequence) -> None:
    def _left_pivot(seq, left, right):
        return left

    _quicksort(seq, 0, len(seq) - 1, _left_pivot)


# Pivots using median-of-three calculation.
def quicksort_mo3(seq: MutableSequence) -> None:
    def _mo3_pivot(seq, left, right):
        middle = (left + right) // 2
        a, b, c = seq[left], seq[middle], seq[right]
        if a <= b <= c:
            median = middle
        elif a <= c <= b:
            median = right
        elif b <= a <= c:
            median = left
        elif b <= c <= a:
            median = right
        elif c <= a <= b:
            median = left
        elif c <= b <= a:
            median = middle
        else:
            raise AssertionError("Median algorithm is broken.")
        return median

    _quicksort(seq, 0, len(seq) - 1, _mo3_pivot)


# Uses 3 partitions.
def quicksort_3w(seq) -> None:
    # Algorithm reference:
    # Chakraborty, Arnab. 2019. "3-Way QuickSort (Dutch National Flag)." Tutorials Point.
    # https://www.tutorialspoint.com/3-way-quicksort-dutch-national-flag

    def _partition(seq, left: int, right: int) -> Tuple[int, int]:
        if right - left <= 1:
            if seq[right] < seq[left]:
                seq[right], seq[left] = seq[left], seq[right]
            return left, right
        else:
            mid = left
            pivot = seq[right]
            while mid <= right:
                if seq[mid] < pivot:
                    seq[left], seq[mid] = seq[mid], seq[left]
                    left += 1
                    mid += 1
                elif seq[mid] == pivot:
                    mid += 1
                elif seq[mid] > pivot:
                    seq[mid], seq[right] = seq[right], seq[mid]
                    right -= 1
            return left - 1, mid

    def _quicksort_3w(seq, left: int, right: int) -> None:
        if left < right:
            i, j = _partition(seq, left, right)
            _quicksort_3w(seq, left, i)
            _quicksort_3w(seq, j, right)

    _quicksort_3w(seq, 0, len(seq) - 1)


def shell_sort(seq) -> None:
    for h in (5, 3, 1):
        for n in range(h, len(seq), h):
            i = n
            while i > 0 and seq[i - h] > seq[i]:
                seq[i], seq[i - h] = seq[i - h], seq[i]
                i -= h


def counting_sort(seq, key=lambda x: x) -> None:
    if seq:
        minimum = min(map(key, seq))
        counts = numpy.zeros(max(map(key, seq)) - minimum + 1, dtype=numpy.int)
        key_ = lambda x: key(x) - minimum
        for e in seq:
            counts[key_(e)] += 1
        acc = 0
        for i in range(len(counts)):
            counts[i], acc = acc, counts[i] + acc
        result = numpy.zeros(len(seq), dtype=numpy.object)
        for e in seq:
            idx = counts[key_(e)]
            result[idx] = e
            counts[key_(e)] += 1
        for i, e in enumerate(result):
            seq[i] = e


def radix_sort_lsd(seq) -> None:
    if seq:
        maximum = max(seq)
        digits = len(str(abs(maximum)))
        for i in range(digits):
            key = lambda x: (x // (10 ** i)) % 10
            counting_sort(seq, key=key)


def _quicksort(seq: MutableSequence, left: int, right: int,
               pivot_selector: Callable[[MutableSequence, int, int], int]) -> None:
    def _partition(seq: MutableSequence, left: int, right: int, pivot: int) -> int:
        pivot_val = seq[pivot]
        seq[pivot] = seq[right]
        seq[right] = pivot_val
        cur = left
        for i in range(left, right):
            if seq[i] < pivot_val:
                seq[i], seq[cur] = seq[cur], seq[i]
                cur += 1
        new_pivot = cur
        seq[right] = seq[new_pivot]
        seq[new_pivot] = pivot_val

        return new_pivot

    if left < right:
        pivot = pivot_selector(seq, left, right)
        new_pivot = _partition(seq, left, right, pivot)
        _quicksort(seq, left, new_pivot - 1, pivot_selector)
        _quicksort(seq, new_pivot + 1, right, pivot_selector)
