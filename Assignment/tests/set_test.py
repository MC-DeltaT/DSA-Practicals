from dsa import Set, SinglyLinkedList

import pickle
import random
from unittest import TestCase


__all__ = [
    "SetTest"
]


class SetTest(TestCase):
    TEST_SIZE = 750

    def setUp(self) -> None:
        # Make sure capacity is low enough to trigger resizes.
        self._set = Set(self.TEST_SIZE // 10)

    def test_add_contains_1(self) -> None:
        # Add unique items.
        for i in random.sample(range(self.TEST_SIZE), self.TEST_SIZE):
            self.assertNotIn(i, self._set, "pre-add contain check")
            self.assertTrue(self._set.add(i))
            self.assertIn(i, self._set, "immediate contain check")

        # Check again to make sure no funky stuff happens after resizes.
        for i in random.sample(range(self.TEST_SIZE), self.TEST_SIZE):
            self.assertIn(i, self._set, "post-resize contain check")

        for i in random.sample(range(self.TEST_SIZE, self.TEST_SIZE * 2), self.TEST_SIZE):
            self.assertNotIn(i, self._set, "non-existent items contain check round 1")

        # Check again to make sure no funky stuff happens.
        for i in random.sample(range(self.TEST_SIZE, self.TEST_SIZE * 2), self.TEST_SIZE):
            self.assertNotIn(i, self._set, "non-existent items contain check round 2")

        # Add duplicate items.
        for i in random.sample(range(self.TEST_SIZE), self.TEST_SIZE):
            self.assertFalse(self._set.add(i))

        for i in random.sample(range(self.TEST_SIZE), self.TEST_SIZE):
            self.assertIn(i, self._set, "duplicate item contain check")

    def test_add_contains_2(self) -> None:
        # Add items in order of hash.
        for i in range(self.TEST_SIZE):
            self.assertTrue(self._set.add(i))
            self.assertIn(i, self._set, "in order immediate contain check")

        for i in random.sample(range(self.TEST_SIZE), self.TEST_SIZE):
            self.assertIn(i, self._set, "in order post-resize contain check")

    def test_add_contains_3(self) -> None:
        # Add items in reverse order of hash.
        for i in reversed(range(self.TEST_SIZE)):
            self.assertTrue(self._set.add(i))
            self.assertIn(i, self._set, "reverse order immediate contain check")

        for i in random.sample(range(self.TEST_SIZE), self.TEST_SIZE):
            self.assertIn(i, self._set, "reverse order post-resize contain check")

    def test_remove(self) -> None:
        for i in range(self.TEST_SIZE):
            with self.assertRaises(KeyError):
                self._set.remove(i)

        for i in random.sample(range(self.TEST_SIZE), self.TEST_SIZE):
            self._set.add(i)

        for i in random.sample(range(self.TEST_SIZE), self.TEST_SIZE):
            self._set.remove(i)
            self.assertNotIn(i, self._set, "immediate contain check")

        # Check again to make sure no funky stuff happens after resizes.
        for i in random.sample(range(self.TEST_SIZE), self.TEST_SIZE):
            self.assertNotIn(i, self._set, "post-resize contain check")

    def test_len(self) -> None:
        size = 0
        self.assertEqual(size, len(self._set), "empty set size")

        for i in random.sample(range(self.TEST_SIZE), self.TEST_SIZE):
            self._set.add(i)
            size += 1
            self.assertEqual(size, len(self._set), "add unique items size check")

        for i in random.sample(range(self.TEST_SIZE), self.TEST_SIZE):
            self._set.add(i)
            self.assertEqual(size, len(self._set), "add duplicate items size check")

        for i in random.sample(range(self.TEST_SIZE), self.TEST_SIZE):
            self._set.remove(i)
            size -= 1
            self.assertEqual(size, len(self._set), "remove items size check")

    def test_iter(self) -> None:
        for _ in self._set:
            self.fail("empty set iter")

        items = SinglyLinkedList()
        # Add unique items.
        for i in random.sample(range(self.TEST_SIZE), self.TEST_SIZE):
            self._set.add(i)
            items.insert_last(i)
            visited = 0
            for item in self._set:
                self.assertIn(item, items, "iter item present")
                visited += 1
            self.assertEqual(visited, len(items), "iter item count")

        # Add duplicate items.
        for i in random.sample(range(self.TEST_SIZE), self.TEST_SIZE):
            self._set.add(i)

        visited = 0
        for item in self._set:
            self.assertIn(item, items, "re-add iter item present")
            visited += 1
        self.assertEqual(visited, len(items), "re-add item item count")

    def test_serialise(self) -> None:
        s = pickle.loads(pickle.dumps(self._set))
        self.assertEqual(0, len(s))
        for _ in s:
            self.fail()

        for i in random.sample(range(self.TEST_SIZE), self.TEST_SIZE):
            self._set.add(i)
        s = pickle.loads(pickle.dumps(self._set))
        self.assertEqual(self.TEST_SIZE, len(s))
        for i in random.sample(range(self.TEST_SIZE), self.TEST_SIZE):
            self.assertIn(i, s)
