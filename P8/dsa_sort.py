from typing import MutableSequence

import numpy


__all__ = [
    "mergesort",
    "quicksort"
]


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


# Sorts seq in place using the quicksort algorithm.
def quicksort(seq: MutableSequence) -> None:
    def _quicksort(seq: MutableSequence, left: int, right: int) -> None:
        if left < right:
            pivot = (left + right) // 2
            new_pivot = _partition(seq, left, right, pivot)
            _quicksort(seq, left, new_pivot - 1)
            _quicksort(seq, new_pivot + 1, right)

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

    _quicksort(seq, 0, len(seq) - 1)
