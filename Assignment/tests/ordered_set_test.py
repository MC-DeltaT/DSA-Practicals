from dsa import Array, OrderedSet, SinglyLinkedList

import random
from unittest import TestCase


__all__ = [
    "OrderedSetTest"
]


class OrderedSetTest(TestCase):
    TEST_SIZE = 2000

    def setUp(self) -> None:
        # Make sure capacity is low enough to trigger resizes.
        self._oset = OrderedSet(self.TEST_SIZE // 10)

    def test_add_first(self) -> None:
        items = Array(random.sample(range(self.TEST_SIZE), self.TEST_SIZE))

        size = 0
        for i in items:
            self._oset.add_first(i)
            size += 1
            self.assertIn(i, self._oset)
            self.assertEqual(size, len(self._oset))

        for i in random.sample(items, self.TEST_SIZE):
            self.assertIn(i, self._oset)
            self.assertEqual(size, len(self._oset))

        for i in random.sample(items, self.TEST_SIZE):
            self._oset.add_first(i)
            self.assertIn(i, self._oset)
            self.assertEqual(size, len(self._oset))

        for i in random.sample(items, self.TEST_SIZE):
            self.assertIn(i, self._oset)
            self.assertEqual(size, len(self._oset))

        for expected, actual in zip(reversed(items), self._oset):
            self.assertEqual(expected, actual)

    def test_add_last(self) -> None:
        items = Array(random.sample(range(self.TEST_SIZE), self.TEST_SIZE))

        size = 0
        for i in items:
            self._oset.add_last(i)
            size += 1
            self.assertIn(i, self._oset)
            self.assertEqual(size, len(self._oset))

        for i in random.sample(items, self.TEST_SIZE):
            self.assertIn(i, self._oset)
            self.assertEqual(size, len(self._oset))

        for i in random.sample(items, self.TEST_SIZE):
            self._oset.add_last(i)
            self.assertIn(i, self._oset)
            self.assertEqual(size, len(self._oset))

        for i in random.sample(items, self.TEST_SIZE):
            self.assertIn(i, self._oset)
            self.assertEqual(size, len(self._oset))

        for expected, actual in zip(items, self._oset):
            self.assertEqual(expected, actual)

    def test_remove(self) -> None:
        items = SinglyLinkedList(random.sample(range(self.TEST_SIZE), self.TEST_SIZE))

        for i in items:
            self._oset.add_last(i)
            self.assertIn(i, self._oset)

        size = len(items)
        for i in random.sample(Array(items), len(items)):
            self._oset.remove(i)
            items.remove(i)
            size -= 1
            self.assertEqual(size, len(self._oset))
            self.assertNotIn(i, self._oset)
            for expected, actual in zip(items, self._oset):
                self.assertEqual(expected, actual)
