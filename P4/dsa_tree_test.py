from dsa_tree import DSABinarySearchTree

from operator import gt, lt
import random
from unittest import TestCase


class DSABinarySearchTreeTest(TestCase):
    test_size = 500

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        random.seed()

    def setUp(self) -> None:
        self._tree = DSABinarySearchTree()

    def test_comparator(self) -> None:
        self.assertIs(lt, self._tree.comparator)
        tree2 = DSABinarySearchTree(gt)
        self.assertIs(gt, tree2.comparator)

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

    def test_max_key(self) -> None:
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
        inserted = []
        count = 0
        for key, value in zip(keys, values):
            self._tree.insert(key, value)
            count += 1
            inserted.append((key, value))
            in_order = list(self._tree.in_order())
            self.assertEqual(count, len(in_order))
            sorted_pairs = sorted(inserted, key=lambda p: p[0])
            for i, (k, v) in enumerate(in_order):
                self.assertEqual(sorted_pairs[i][0], k)
                self.assertEqual(sorted_pairs[i][1], v)

        keys = random.sample(range(self.test_size), self.test_size)
        for key in keys:
            value = self._tree.find(key)
            self._tree.delete(key)
            count -= 1
            inserted.remove((key, value))
            in_order = list(self._tree.in_order())
            self.assertEqual(count, len(in_order))
            sorted_pairs = sorted(inserted, key=lambda p: p[0])
            for i, (k, v) in enumerate(in_order):
                self.assertEqual(sorted_pairs[i][0], k)
                self.assertEqual(sorted_pairs[i][1], v)

    def test_pre_order(self) -> None:
        for _ in self._tree.pre_order():
            self.fail()

        keys = random.sample(range(self.test_size), self.test_size)
        values = random.sample(range(self.test_size), self.test_size)
        inserted = []
        count = 0
        for key, value in zip(keys, values):
            self._tree.insert(key, value)
            count += 1
            inserted.append((key, value))
            pre_order = list(self._tree.pre_order())
            self.assertEqual(count, len(pre_order))
            visited_keys = set()
            visited_values = set()
            for k, v in pre_order:
                self.assertFalse(k in visited_keys)
                self.assertFalse(v in visited_values)
                visited_keys.add(k)
                visited_values.add(v)
            tree2 = DSABinarySearchTree(self._tree.comparator)
            for k, v in pre_order:
                tree2.insert(k, v)
            self.assertEqual(pre_order, list(tree2.pre_order()))
            self.assertEqual(list(self._tree.in_order()), list(tree2.in_order()))
            del tree2

        for key in random.sample(range(self.test_size), self.test_size):
            value = self._tree.find(key)
            self._tree.delete(key)
            count -= 1
            inserted.remove((key, value))
            pre_order = list(self._tree.pre_order())
            self.assertEqual(count, len(pre_order))
            visited_keys = set()
            visited_values = set()
            for k, v in pre_order:
                self.assertFalse(k in visited_keys)
                self.assertFalse(v in visited_values)
                visited_keys.add(k)
                visited_values.add(v)
            tree2 = DSABinarySearchTree(self._tree.comparator)
            for k, v in pre_order:
                tree2.insert(k, v)
            self.assertEqual(pre_order, list(tree2.pre_order()))
            self.assertEqual(list(self._tree.in_order()), list(tree2.in_order()))
            del tree2

    def test_post_order(self) -> None:
        for _ in self._tree.post_order():
            self.fail()

        keys = random.sample(range(self.test_size), self.test_size)
        values = random.sample(range(self.test_size), self.test_size)
        inserted = []
        count = 0
        for key, value in zip(keys, values):
            self._tree.insert(key, value)
            count += 1
            inserted.append((key, value))
            post_order = list(self._tree.post_order())
            self.assertEqual(count, len(post_order))
            visited_keys = set()
            visited_values = set()
            for k, v in post_order:
                self.assertFalse(k in visited_keys)
                self.assertFalse(v in visited_values)
                visited_keys.add(k)
                visited_values.add(v)

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
        for key in [50, 40, 60, 30, 45, 55, 65, 70]:
            self._tree.insert(key, key)
            self.assertEqual(1.0, self._tree.balance())
        for key in [75, 10, 80, 47]:
            self._tree.insert(key, key)
            self.assertTrue(0.0 < self._tree.balance() < 1.0)
        for key in range(100, 150):
            self._tree.insert(key, key)
        for key in range(150, 150 + self.test_size):
            self._tree.insert(key, key)
            self.assertLessEqual(self._tree.balance(), 0.25)
