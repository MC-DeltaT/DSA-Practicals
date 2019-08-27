from dsa_linked_list import DSALinkedList

import pickle
from unittest import TestCase


class DSALinkedListTest(TestCase):
    test_size = 10

    def setUp(self) -> None:
        self._list = DSALinkedList()

    def test_insert_first(self) -> None:
        for i in range(self.test_size):
            self._list.insert_first(i)
            self.assertEqual(i, self._list.peek_first())
            self.assertEqual(0, self._list.peek_last())

    def test_insert_last(self) -> None:
        for i in range(self.test_size):
            self._list.insert_last(i)
            self.assertEqual(i, self._list.peek_last())
            self.assertEqual(0, self._list.peek_first())

    def test_remove_first(self) -> None:
        with self.assertRaises(ValueError):
            self._list.remove_first()

        for i in range(self.test_size):
            self._list.insert_last(i)
        for i in range(self.test_size):
            self.assertEqual(self.test_size - 1, self._list.peek_last())
            self.assertEqual(i, self._list.peek_first())
            self._list.remove_first()

        with self.assertRaises(ValueError):
            self._list.remove_first()

    def test_remove_last(self) -> None:
        with self.assertRaises(ValueError):
            self._list.remove_last()

        for i in range(self.test_size):
            self._list.insert_last(i)
        for i in reversed(range(self.test_size)):
            self.assertEqual(0, self._list.peek_first())
            self.assertEqual(i, self._list.peek_last())
            self._list.remove_last()

        with self.assertRaises(ValueError):
            self._list.remove_last()

    def test_remove_all(self) -> None:
        self._list.remove_all()

        self._list.insert_first(42)
        self._list.remove_all()
        self.assertTrue(self._list.is_empty())

        for i in range(self.test_size):
            self._list.insert_first(i)
        self._list.remove_all()
        self.assertTrue(self._list.is_empty()) 

    def test_is_empty(self) -> None:
        self.assertTrue(self._list.is_empty())

        for i in range(self.test_size):
            self._list.insert_last(i)
            self.assertFalse(self._list.is_empty())
        for i in range(self.test_size):
            self.assertFalse(self._list.is_empty())
            self._list.remove_last()
        self.assertTrue(self._list.is_empty())

        for i in range(self.test_size):
            self._list.insert_first(i)
            self.assertFalse(self._list.is_empty())
        for i in range(self.test_size):
            self.assertFalse(self._list.is_empty())
            self._list.remove_first()
        self.assertTrue(self._list.is_empty())

    def test_iter(self) -> None:
        for e in self._list:
            self.fail()

        for i in range(self.test_size):
            self._list.insert_last(i)
            for j, e in enumerate(self._list):
                self.assertEqual(j, e)

    def test_reversed(self) -> None:
        for e in reversed(self._list):
            self.fail()

        for i in range(self.test_size):
            self._list.insert_first(i)
            for j, e in enumerate(reversed(self._list)):
                self.assertEqual(j, e)

    def test_serialize(self) -> None:
        s = pickle.dumps(self._list)
        self._list = pickle.loads(s)
        self.assertTrue(self._list.is_empty())

        for i in range(self.test_size):
            self._list.insert_last(i)
        s = pickle.dumps(self._list)
        self._list = pickle.loads(s)
        self.assertFalse(self._list.is_empty())
        for i in range(self.test_size):
            self.assertEqual(i, self._list.peek_first())
            self._list.remove_first()
