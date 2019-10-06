from dsa_sort import *

import random
import unittest


class DSASortTest(unittest.TestCase):
    TEST_SIZE = 2000

    def test_mergesort(self) -> None:
        for n in range(self.TEST_SIZE):
            array = random.choices(range(self.TEST_SIZE), k=n)
            expected = sorted(array)
            mergesort(array)
            self.assertListEqual(expected, array)

    def test_quicksort(self) -> None:
        for n in range(self.TEST_SIZE):
            array = random.choices(range(self.TEST_SIZE), k=n)
            expected = sorted(array)
            quicksort(array)
            self.assertListEqual(expected, array)


if __name__ == "__main__":
    unittest.main()
