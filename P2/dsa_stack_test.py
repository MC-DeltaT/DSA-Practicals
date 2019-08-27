from dsa_stack import DSAStack

from unittest import TestCase


class DSAStackTest(TestCase):
    max_stack_size = 10

    def setUp(self) -> None:
        self._stack = DSAStack(self.max_stack_size)

    def test_push(self) -> None:
        for i in range(self.max_stack_size):
            self._stack.push(i)
            self.assertEqual(i, self._stack.top())
        with self.assertRaises(ValueError):
            self._stack.push(42)

    def test_pop(self) -> None:
        with self.assertRaises(ValueError):
            self._stack.pop()
        for i in range(self.max_stack_size):
            self._stack.push(i)
        for i in range(self.max_stack_size - 1, -1, -1):
            val = self._stack.pop()
            self.assertEqual(i, val)
        with self.assertRaises(ValueError):
            self._stack.pop()

    def test_is_empty(self) -> None:
        self.assertTrue(self._stack.is_empty())
        for i in range(self.max_stack_size):
            self._stack.push(i)
            self.assertFalse(self._stack.is_empty())
        for i in range(self.max_stack_size):
            self.assertFalse(self._stack.is_empty())
            self._stack.pop()
        self.assertTrue(self._stack.is_empty())

    def test_is_full(self) -> None:
        for i in range(self.max_stack_size):
            self.assertFalse(self._stack.is_full())
            self._stack.push(i)
        self.assertTrue(self._stack.is_full())
        for i in range(self.max_stack_size):
            self._stack.pop()
            self.assertFalse(self._stack.is_full())

    def test_get_size(self) -> None:
        self.assertEqual(0, self._stack.get_size())
        for i in range(self.max_stack_size):
            self._stack.push(i)
            self.assertEqual(i + 1, self._stack.get_size())
        for i in range(self.max_stack_size - 1, -1, -1):
            self._stack.pop()
            self.assertEqual(i, self._stack.get_size())
