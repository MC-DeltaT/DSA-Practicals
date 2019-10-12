# Sourced from my Data Structures & Algorithms practical worksheet 8 submission,
# with modifications.

from dsa import Array
from dsa.sorting import *

import random
from typing import Sequence
from unittest import TestCase


__all__ = [
    "SortingTest"
]


class SortingTest(TestCase):
    TEST_SIZE = 500

    def test_mergesort(self) -> None:
        self.sortTester(mergesort)

    def test_quicksort(self) -> None:
        self.sortTester(quicksort)

    def sortTester(self, sorter) -> None:
        for n in range(self.TEST_SIZE):
            data = Array(range(n))
            actual = data.copy()
            sorter(actual)
            self.assertArrayEqual(sorted(data), actual)

        for n in range(self.TEST_SIZE):
            data = Array(range(n, -1, -1))
            actual = data.copy()
            sorter(actual)
            self.assertArrayEqual(sorted(data), actual)

        for n in range(self.TEST_SIZE):
            data = random.choices(range(self.TEST_SIZE), k=n)
            actual = data.copy()
            sorter(actual)
            self.assertArrayEqual(sorted(data), actual)

        for n in range(self.TEST_SIZE):
            data = random.choices(range(self.TEST_SIZE), k=n)
            actual = data.copy()
            sorter(actual, reverse=True)
            self.assertArrayEqual(sorted(data, reverse=True), actual)

    def assertArrayEqual(self, arr1: Sequence, arr2: Sequence) -> None:
        self.assertEqual(len(arr1), len(arr2))
        for a, b in zip(arr1, arr2):
            self.assertEqual(a, b)
