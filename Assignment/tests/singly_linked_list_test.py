# Sourced from my Data Structures & Algorithms practical worksheet 3 submission,
# with modifications.

from dsa import SinglyLinkedList

import pickle
import random
from unittest import TestCase


__all__ = [
    "SinglyLinkedListTest"
]


class SinglyLinkedListTest(TestCase):
    TEST_SIZE = 200

    def setUp(self) -> None:
        self._list = SinglyLinkedList()

    def test_init(self) -> None:
        data = range(self.TEST_SIZE)
        l = SinglyLinkedList(data)
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

    def test_remove_all(self) -> None:
        self._list.remove_all()

        self._list.insert_first(42)
        self._list.remove_all()
        self.assertEqual(0, len(self._list))

        for i in range(self.TEST_SIZE):
            self._list.insert_first(i)
        self._list.remove_all()
        self.assertEqual(0, len(self._list))

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

        # Make sure removing doesn't mess up further operations.
        for i in range(self.TEST_SIZE):
            self._list.insert_first(i)
        for expected, actual in zip(reversed(range(self.TEST_SIZE)), self._list):
            self.assertEqual(expected, actual)

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

        for _ in range(self.TEST_SIZE * 2):
            self._list.remove_first()
            size -= 1
            self.assertEqual(size, len(self._list))

    def test_iter(self) -> None:
        for _ in self._list:
            self.fail()

        for i in range(self.TEST_SIZE):
            self._list.insert_last(i)
            for j, e in enumerate(self._list):
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

    def test_serialise(self) -> None:
        ll = pickle.loads(pickle.dumps(self._list))
        self.assertEqual(0, len(ll))
        for _ in ll:
            self.fail()

        for i in range(self.TEST_SIZE):
            self._list.insert_first(i)
        ll = pickle.loads(pickle.dumps(self._list))
        self.assertEqual(self.TEST_SIZE, len(ll))
        for expected, actual in zip(reversed(range(self.TEST_SIZE)), ll):
            self.assertEqual(expected, actual)
