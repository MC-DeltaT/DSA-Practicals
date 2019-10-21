from dsa import Array

import random
from unittest import TestCase


__all__ = [
    "ArrayTest"
]


class ArrayTest(TestCase):
    TEST_SIZE = 10000

    def setUp(self) -> None:
        self._array = Array(self.TEST_SIZE)

    def test_init(self) -> None:
        array = Array([])
        self.assertEqual(0, len(array))
        for _ in array:
            self.fail()
        with self.assertRaises(IndexError):
            for i in range(self.TEST_SIZE):
                _ = array[i]
        with self.assertRaises(IndexError):
            for i in range(self.TEST_SIZE):
                array[i] = i

        array = Array(range(self.TEST_SIZE))
        self.assertEqual(self.TEST_SIZE, len(array))
        for i in range(self.TEST_SIZE):
            self.assertEqual(i, array[i])
        for expected, actual in zip(range(self.TEST_SIZE), array):
            self.assertEqual(expected, actual)

    def test_setitem(self) -> None:
        data = random.choices(range(self.TEST_SIZE), k=self.TEST_SIZE)
        for i, item in enumerate(data):
            self._array[i] = item
        for i in random.sample(range(self.TEST_SIZE), k=self.TEST_SIZE):
            self.assertEqual(data[i], self._array[i])
        for expected, actual in zip(data, self._array):
            self.assertEqual(expected, actual)
        with self.assertRaises(IndexError):
            for i in range(self.TEST_SIZE, self.TEST_SIZE * 2):
                self._array[i] = i

    def test_reversed(self) -> None:
        data = random.choices(range(self.TEST_SIZE), k=self.TEST_SIZE)
        for i, item in enumerate(data):
            self._array[i] = item
        for expected, actual in zip(reversed(data), reversed(self._array)):
            self.assertEqual(expected, actual)

    def test_copy(self) -> None:
        for i in range(self.TEST_SIZE):
            self._array[i] = object()
        copy = self._array.copy()
        self.assertIsNot(copy, self._array)
        for o1, o2 in zip(self._array, copy):
            self.assertIs(o1, o2)
