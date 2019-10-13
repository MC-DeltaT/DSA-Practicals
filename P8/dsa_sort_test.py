from dsa_sort import *

import random
from typing import Callable, MutableSequence
import unittest


class DSASortTest(unittest.TestCase):
    TEST_SIZE = 300

    def test_bubble_sort(self) -> None:
        self.sortTester(bubble_sort)

    def test_insertion_sort(self) -> None:
        self.sortTester(insertion_sort)

    def test_selection_sort(self) -> None:
        self.sortTester(selection_sort)

    def test_mergesort(self) -> None:
        self.sortTester(mergesort)

    def test_quicksort_bad(self) -> None:
        self.sortTester(quicksort_bad)

    def test_quicksort_mo3(self) -> None:
        self.sortTester(quicksort_mo3)

    def test_quicksort_3w(self) -> None:
        self.sortTester(quicksort_3w)

    def sortTester(self, sorter: Callable[[MutableSequence], None]) -> None:
        for n in range(self.TEST_SIZE):
            array = list(range(self.TEST_SIZE))
            expected = sorted(array)
            sorter(array)
            self.assertListEqual(expected, array)

        for n in range(self.TEST_SIZE):
            array = list(reversed(range(self.TEST_SIZE)))
            expected = sorted(array)
            sorter(array)
            self.assertListEqual(expected, array)

        for n in range(self.TEST_SIZE):
            array = random.choices(range(self.TEST_SIZE), k=n)
            expected = sorted(array)
            sorter(array)
            self.assertListEqual(expected, array)


if __name__ == "__main__":
    unittest.main()
