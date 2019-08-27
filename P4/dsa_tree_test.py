from dsa_tree import DSABinarySearchTree

import random
from unittest import TestCase


class DSABinarySearchTreeTest(TestCase):
    test_size = 10

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        random.seed()

    def setUp(self) -> None:
        self._tree = DSABinarySearchTree()

    def test_insert_find(self) -> None:
        for key in range(self.test_size):
            with self.assertRaises(ValueError):
                self._tree.find(key)

        keys = random.sample(range(self.test_size), self.test_size)
        values = random.sample(range(self.test_size), self.test_size)
        for key, value in zip(keys, values):
            self._tree.insert(key, value)
        tmp = list(zip(keys, values))
        random.shuffle(tmp)
        keys, values = zip(*tmp)
        for key, value in zip(keys, values):
            self.assertEqual(value, self._tree.find(key))

        for key in random.sample(range(self.test_size), self.test_size):
            with self.assertRaises(ValueError):
                self._tree.insert(key, key)

    def test_delete(self) -> None:
        for i in range(self.test_size):
            with self.assertRaises(ValueError):
                self._tree.delete(i)

        for key, value in zip(random.sample(range(self.test_size), self.test_size),
                              random.sample(range(self.test_size), self.test_size)):
            self._tree.insert(key, value)
        for key in random.sample(range(self.test_size), self.test_size):
            self._tree.delete(key)
            with self.assertRaises(ValueError):
                self._tree.find(key)

    def test_is_empty(self) -> None:
        self.assertTrue(self._tree.is_empty())

        for key, value in zip(random.sample(range(self.test_size), self.test_size),
                              random.sample(range(self.test_size), self.test_size)):
            self._tree.insert(key, value)
            self.assertFalse(self._tree.is_empty())
        for key in random.sample(range(self.test_size), self.test_size):
            self.assertFalse(self._tree.is_empty())
            self._tree.delete(key)

        self.assertTrue(self._tree.is_empty())

    def test_height(self) -> None:
        height = 0
        self.assertEqual(height, self._tree.height())

        self._tree.insert(self.test_size, self.test_size)
        height += 1
        self.assertEqual(height, self._tree.height())

        # Insert left children only.
        for key in reversed(range(self.test_size)):
            self._tree.insert(key, key)
            height += 1
            self.assertEqual(height, self._tree.height())

        # Insert right children only.
        for key in range(self.test_size + 1, 2 * self.test_size + 1):
            self._tree.insert(key, key)
            self.assertEqual(height, self._tree.height())

        # Delete left children only.
        for key in range(self.test_size):
            self._tree.delete(key)
            self.assertEqual(height, self._tree.height())

        # Delete right children only.
        for key in range(self.test_size + 1, 2 * self.test_size + 1):
            self._tree.delete(key)
            height -= 1
            self.assertEqual(height, self._tree.height())

        self._tree.delete(self.test_size)
        height -= 1
        self.assertEqual(height, self._tree.height())

        for key, height in [(50, 1), (40, 2), (30, 3), (60, 3), (55, 3), (57, 4)]:
            self._tree.insert(key, key)
            self.assertEqual(height, self._tree.height())

    def test_min_key(self) -> None:
        with self.assertRaises(ValueError):
            self._tree.min_key()

        inserted_keys = set()
        for key, value in zip(random.sample(range(self.test_size), self.test_size),
                              random.sample(range(self.test_size), self.test_size)):
            self._tree.insert(key, value)
            inserted_keys.add(key)
            self.assertEqual(min(inserted_keys), self._tree.min_key())

        for key in random.sample(range(self.test_size), self.test_size):
            self.assertEqual(min(inserted_keys), self._tree.min_key())
            self._tree.delete(key)
            inserted_keys.remove(key)

        with self.assertRaises(ValueError):
            self._tree.min_key()

    def test_max(self) -> None:
        with self.assertRaises(ValueError):
            self._tree.max_key()

        inserted_keys = set()
        for key, value in zip(random.sample(range(self.test_size), self.test_size),
                              random.sample(range(self.test_size), self.test_size)):
            self._tree.insert(key, value)
            inserted_keys.add(key)
            self.assertEqual(max(inserted_keys), self._tree.max_key())

        for key in random.sample(range(self.test_size), self.test_size):
            self.assertEqual(max(inserted_keys), self._tree.max_key())
            self._tree.delete(key)
            inserted_keys.remove(key)

        with self.assertRaises(ValueError):
            self._tree.max_key()

    def test_in_order(self) -> None:
        for _ in self._tree.in_order():
            self.fail()

        keys = random.sample(range(self.test_size), self.test_size)
        values = random.sample(range(self.test_size), self.test_size)
        inserted_keys = []
        inserted_values = []
        count = 0
        for key, value in zip(keys, values):
            self._tree.insert(key, value)
            count += 1
            inserted_keys.append(key)
            inserted_values.append(value)
            sorted_keys, sorted_values = zip(*sorted(zip(inserted_keys, inserted_values)))
            in_order = list(self._tree.in_order())
            self.assertEqual(count, len(in_order))
            for j, (k, v) in enumerate(in_order):
                self.assertEqual(sorted_keys[j], k)
                self.assertEqual(sorted_values[j], v)

            # for i in random.sample(range(n), n):
            #     sorted_keys, sorted_values = zip(*sorted(zip(keys, values)))
            #     in_order = list(self._tree.in_order())
            #     self.assertEqual(n, len(in_order))
            #     for j, (key, value) in enumerate(in_order):
            #         self.assertEqual(sorted_keys[j], key)
            #         self.assertEqual(sorted_values[j], value)
            #     self._tree.delete(keys[i])
            #     del keys[i]
            #     del values[i]

    def test_len(self) -> None:
        size = 0
        self.assertEqual(size, len(self._tree))

        for key, value in zip(random.sample(range(self.test_size), self.test_size),
                              random.sample(range(self.test_size), self.test_size)):
            self._tree.insert(key, value)
            size += 1
            self.assertEqual(size, len(self._tree))

        for key in random.sample(range(self.test_size), self.test_size):
            self._tree.delete(key)
            size -= 1
            self.assertEqual(size, len(self._tree))

    def test_balance(self) -> None:
        self.assertEqual(1.0, self._tree.balance())
        for keys, balance in [([50], 1.0), ([40, 60], 1.0), ([30, 45, 55, 65], 1.0)]:
            for key in keys:
                self._tree.insert(key, key)
            self.assertEqual(balance, self._tree.balance())
