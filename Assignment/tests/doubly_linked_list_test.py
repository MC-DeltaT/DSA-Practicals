# Sourced from my Data Structures & Algorithms practical worksheet 3 submission,
# with modifications.

from dsa import DoublyLinkedList

import pickle
import random
from unittest import TestCase


__all__ = [
    "DoublyLinkedListTest"
]


class DoublyLinkedListTest(TestCase):
    TEST_SIZE = 1000

    def setUp(self) -> None:
        self._list = DoublyLinkedList()

    def test_init(self) -> None:
        data = range(self.TEST_SIZE)
        l = DoublyLinkedList(data)
        for expected, actual in zip(data, l):
            self.assertEqual(expected, actual)

    def test_insert_first(self) -> None:
        for i in range(self.TEST_SIZE):
            self._list.insert_first(i)
            self.assertEqual(i, self._list.peek_first())
            self.assertEqual(0, self._list.peek_last())

    def test_insert_last(self) -> None:
        for i in range(self.TEST_SIZE):
            self._list.insert_last(i)
            self.assertEqual(i, self._list.peek_last())
            self.assertEqual(0, self._list.peek_first())

    def test_remove_first(self) -> None:
        with self.assertRaises(ValueError):
            self._list.remove_first()

        for i in range(self.TEST_SIZE):
            self._list.insert_last(i)
        for i in range(self.TEST_SIZE):
            self.assertEqual(self.TEST_SIZE - 1, self._list.peek_last())
            self.assertEqual(i, self._list.peek_first())
            self._list.remove_first()

        with self.assertRaises(ValueError):
            self._list.remove_first()

    def test_remove_last(self) -> None:
        with self.assertRaises(ValueError):
            self._list.remove_last()

        for i in range(self.TEST_SIZE):
            self._list.insert_last(i)
        for i in reversed(range(self.TEST_SIZE)):
            self.assertEqual(0, self._list.peek_first())
            self.assertEqual(i, self._list.peek_last())
            self._list.remove_last()

        with self.assertRaises(ValueError):
            self._list.remove_last()

    def test_remove_all(self) -> None:
        self._list.remove_all()

        self._list.insert_first(42)
        self._list.remove_all()
        self.assertTrue(self._list.is_empty)

        for i in range(self.TEST_SIZE):
            self._list.insert_first(i)
        self._list.remove_all()
        self.assertTrue(self._list.is_empty)

    def test_remove(self) -> None:
        for i in range(self.TEST_SIZE):
            with self.assertRaises(ValueError):
                self._list.remove(i)

        for i in range(self.TEST_SIZE):
            self._list.insert_last(i)

        for i in random.sample(range(self.TEST_SIZE), self.TEST_SIZE):
            self._list.remove(i)
            self.assertNotIn(i, self._list)

        for i in range(self.TEST_SIZE):
            with self.assertRaises(ValueError):
                self._list.remove(i)

    def test_is_empty(self) -> None:
        self.assertTrue(self._list.is_empty)

        for i in range(self.TEST_SIZE):
            self._list.insert_last(i)
            self.assertFalse(self._list.is_empty)
        for i in range(self.TEST_SIZE):
            self.assertFalse(self._list.is_empty)
            self._list.remove_last()
        self.assertTrue(self._list.is_empty)

        for i in range(self.TEST_SIZE):
            self._list.insert_first(i)
            self.assertFalse(self._list.is_empty)
        for i in range(self.TEST_SIZE):
            self.assertFalse(self._list.is_empty)
            self._list.remove_first()
        self.assertTrue(self._list.is_empty)

    def test_copy(self) -> None:
        for _ in self._list.copy():
            self.fail()

        for i in range(self.TEST_SIZE):
            self._list.insert_last(i)
            copy = self._list.copy()
            self.assertFalse(copy is self._list)
            for e1, e2 in zip(self._list, copy):
                self.assertTrue(e1 is e2)

    def test_len(self) -> None:
        size = 0
        self.assertEqual(size, len(self._list))

        for i in range(self.TEST_SIZE):
            self._list.insert_first(i)
            size += 1
            self.assertEqual(size, len(self._list))

        for i in range(self.TEST_SIZE):
            self._list.insert_last(i)
            size += 1
            self.assertEqual(size, len(self._list))

        for _ in range(self.TEST_SIZE):
            self._list.remove_first()
            size -= 1
            self.assertEqual(size, len(self._list))

        for _ in range(self.TEST_SIZE):
            self._list.remove_last()
            size -= 1
            self.assertEqual(size, len(self._list))

    def test_iter(self) -> None:
        for _ in self._list:
            self.fail()

        for i in range(self.TEST_SIZE):
            self._list.insert_last(i)
            for j, e in enumerate(self._list):
                self.assertEqual(j, e)

    def test_reversed(self) -> None:
        for _ in reversed(self._list):
            self.fail()

        for i in range(self.TEST_SIZE):
            self._list.insert_first(i)
            for j, e in enumerate(reversed(self._list)):
                self.assertEqual(j, e)

    def test_contains(self) -> None:
        for i in range(self.TEST_SIZE):
            self.assertNotIn(i, self._list)

        for i in range(self.TEST_SIZE):
            self._list.insert_last(i)
            self.assertIn(i, self._list)

        for i in range(self.TEST_SIZE):
            self.assertIn(i, self._list)

        for i in range(self.TEST_SIZE, self.TEST_SIZE * 2):
            self.assertNotIn(i, self._list)
