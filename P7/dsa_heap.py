# I've structured the heap implementation slightly differently to the layout in
# the prac worksheet.
# Most of the heap operations can work on any sequence type, so they're
# implemented as free functions instead.
# Same with heapsort, which doesn't really make sense to be an instance method
# of the heap class.


from functools import total_ordering
from typing import Any, MutableSequence

import numpy


__all__ = [
    "DSAHeap",
    "HeapEntry",
    "heapify",
    "heapsort"
]


@total_ordering
class HeapEntry:
    # priority must support ordering via the < operator.
    def __init__(self, obj: Any, priority) -> None:
        self.obj = obj
        self.priority = priority

    def __lt__(self, other) -> bool:
        return isinstance(other, HeapEntry) and self.priority < other.priority

    def __repr__(self) -> str:
        return f"priority={self.priority}, obj={self.obj}"


class DSAHeap:
    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError(f"capacity must be >=1, but got {capacity}.")
        self._array = numpy.empty(capacity, dtype=numpy.object)
        self._size = 0

    @property
    def size(self) -> int:
        return self._size

    @property
    def capacity(self) -> int:
        return self._array.size

    @property
    def is_empty(self) -> bool:
        return self.size == 0

    @property
    def is_full(self) -> bool:
        return self.size == self.capacity

    def add(self, obj: Any, priority) -> None:
        if self.is_full:
            raise ValueError("Heap is full.")
        self._array[self._size] = HeapEntry(obj, priority)
        self._size += 1
        _trickle_up(self._array, 0, self._size)

    def remove(self) -> Any:
        if self.is_empty:
            raise ValueError("Heap is empty.")
        res = self._array[0].obj

        self._size -= 1
        self._array[0] = self._array[self._size]
        self._array[self._size] = None
        _trickle_down(self._array, 0, self._size)
        return res


# Reorders a sequence in place such that it forms a max heap.
def heapify(seq: MutableSequence) -> None:
    # Start at last non-leaf node (leaves will always get heapified anyway).
    for i in reversed(range(len(seq) // 2)):
        _trickle_down(seq, i)


# Sorts a sequence in place.
def heapsort(seq: MutableSequence) -> None:
    heapify(seq)
    for i in reversed(range(1, len(seq))):
        seq[0], seq[i] = seq[i], seq[0]
        _trickle_down(seq, 0, i)


def _parent_index(node: int) -> int:
    return (node - 1) // 2


def _left_child_index(node: int) -> int:
    assert node >= 0
    return 2 * node + 1


def _right_child_index(node: int) -> int:
    assert node >= 0
    return 2 * node + 2


# Reforms a max heap on seq[start:stop], given that seq[(start+1):stop] already forms a max heap.
def _trickle_down(seq: MutableSequence, start: int = 0, stop: int = None) -> None:
    def __trickle_down(seq: MutableSequence, start: int, stop: int) -> None:
        assert start >= 0
        assert stop >= 0
        left_child = _left_child_index(start)
        if left_child < stop:
            right_child = _right_child_index(start)
            if right_child < stop:
                max_child = max(left_child, right_child, key=lambda idx: seq[idx])
            else:
                max_child = left_child
            if seq[start] < seq[max_child]:
                seq[start], seq[max_child] = seq[max_child], seq[start]
                __trickle_down(seq, max_child, stop)

    if stop is None:
        stop = len(seq)
    __trickle_down(seq, start, stop)


# Reforms a max heap on seq[start:stop], given that seq[start:(stop-1)] already forms a max heap.
def _trickle_up(seq: MutableSequence, start: int = 0, stop: int = None) -> None:
    def __trickle_up(seq: MutableSequence, start: int, stop: int) -> None:
        assert start >= 0
        parent = _parent_index(stop)
        if parent >= start:
            if seq[parent] < seq[stop]:
                seq[stop], seq[parent] = seq[parent], seq[stop]
            __trickle_up(seq, start, parent)

    if stop is None:
        stop = len(seq)
    __trickle_up(seq, start, stop - 1)
