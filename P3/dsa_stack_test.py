from dsa_stack import DSAStack

from unittest import TestCase


class DSAStackTest(TestCase):
    test_size = 10

    def setUp(self) -> None:
        self._stack = DSAStack()

    def test_push(self) -> None:
        for i in range(self.test_size):
            self._stack.push(i)
            self.assertEqual(i, self._stack.top())

    def test_pop(self) -> None:
        with self.assertRaises(ValueError):
            self._stack.pop()

        for i in range(self.test_size):
            self._stack.push(i)
        for i in reversed(range(self.test_size)):
            val = self._stack.pop()
            self.assertEqual(i, val)

        with self.assertRaises(ValueError):
            self._stack.pop()

    def test_is_empty(self) -> None:
        self.assertTrue(self._stack.is_empty())

        for i in range(self.test_size):
            self._stack.push(i)
            self.assertFalse(self._stack.is_empty())
        for i in range(self.test_size):
            self.assertFalse(self._stack.is_empty())
            self._stack.pop()

        self.assertTrue(self._stack.is_empty())

    def test_iter(self) -> None:
        for e in self._stack:
            self.fail()

        for i in range(self.test_size):
            self._stack.push(i)
            for j, e in enumerate(self._stack):
                self.assertEqual(i - j, e)
