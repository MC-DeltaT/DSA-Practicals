# Sourced from my Data Structures & Algorithms practical worksheet 6 submission,
# with modifications.

from dsa import Array, HashTable

import pickle
import random
from typing import Any, Sequence, Tuple
from unittest import TestCase


__all__ = [
    "HashTableTest"
]


class HashTableTest(TestCase):
    TEST_SIZE = 1000

    def setUp(self) -> None:
        # Make sure capacity is low enough to trigger resizes.
        self._hashtable = HashTable(self.TEST_SIZE // 10)

    def test_next_prime(self) -> None:
        # Assert next prime from non-prime is correct.
        for x, y in [(1, 2), (4, 5), (6, 7), (8, 11), (9, 11), (10, 11), (12, 13), (14, 17), (15, 17), (16, 17), (18, 19)]:
            self.assertEqual(y, HashTable._next_prime(x))

        # Assert next prime from prime is correct.
        for x, y in [(2, 3), (3, 5), (5, 7), (7, 11), (11, 13), (13, 17), (17, 19)]:
            self.assertEqual(y, HashTable._next_prime(x))

        # Assert out-of-range numbers are handled correctly.
        for x in range(-20, 2):
            self.assertEqual(2, HashTable._next_prime(x))

    def test_prev_prime(self) -> None:
        # Assert previous prime from non-prime is correct.
        for x, y in [(4, 3), (6, 5), (8, 7), (9, 7), (10, 7), (12, 11), (14, 13), (15, 13), (16, 13), (18, 17), (19, 17)]:
            self.assertEqual(y, HashTable._prev_prime(x))

        # Assert previous prime from prime is correct.
        for x, y in [(2, 2), (3, 2), (5, 3), (7, 5), (11, 7), (13, 11), (17, 13), (19, 17)]:
            self.assertEqual(y, HashTable._prev_prime(x))

        # Assert out-of-range numbers are handled correctly.
        for x in range(-20, 2):
            self.assertEqual(2, HashTable._next_prime(x))

    def test_set_get_contains(self) -> None:
        keys = Array(random.sample(range(self.TEST_SIZE), self.TEST_SIZE))

        # Assert nothing in table yet.
        for key in keys:
            with self.assertRaises(KeyError):
                _ = self._hashtable[key]
            self.assertNotIn(key, self._hashtable)

        # Assert key, value pairs are correct before any internal resize occurs.
        pairs: Array[Tuple[int, int]] = Array(len(keys))
        for i, key in enumerate(keys):
            value = random.choice(range(self.TEST_SIZE))
            self.assertTrue(self._hashtable.set(key, value))
            pairs[i] = (key, value)
            self.assertEqual(value, self._hashtable[key])
            self.assertIn(key, self._hashtable)

        # Assert key, values pairs are correct after internal resize.
        random.shuffle(pairs)
        for key, value in pairs:
            self.assertEqual(value, self._hashtable[key])
            self.assertIn(key, self._hashtable)

        # Change some values of existing keys.
        for i in random.sample(range(len(pairs)), len(pairs) // 2):
            key, value = pairs[i][0], pairs[i][1]
            value += self.TEST_SIZE
            pairs[i] = (key, value)
            self.assertFalse(self._hashtable.set(key, value))
            self.assertEqual(value, self._hashtable[key])
            self.assertIn(key, self._hashtable)

        # Assert keys still map to correct values after all changes.
        random.shuffle(pairs)
        for key, value in pairs:
            self.assertEqual(value, self._hashtable[key])
            self.assertIn(key, self._hashtable)

    def test_delitem(self) -> None:
        keys = Array(random.sample(range(self.TEST_SIZE), self.TEST_SIZE))

        # Assert can't delete non-existent keys.
        for key in keys:
            with self.assertRaises(KeyError):
                del self._hashtable[key]

        # Add key, value pairs.
        for key in keys:
            value = random.choice(range(self.TEST_SIZE))
            self._hashtable[key] = value

        # Delete entries and assert they got removed.
        random.shuffle(keys)
        for i in range(len(keys)):
            del self._hashtable[keys[i]]
            self.assertNotIn(keys[i], self._hashtable)
            with self.assertRaises(KeyError):
                _ = self._hashtable[keys[i]]
            # Assert rest of entries stayed in hashtable.
            for j in range(i + 1, len(keys)):
                self.assertIn(keys[j], self._hashtable)

        # Assert entries stayed removed after internal resize occurs.
        random.shuffle(keys)
        for key in keys:
            self.assertNotIn(key, self._hashtable)
            with self.assertRaises(KeyError):
                _ = self._hashtable[key]

        # Assert can't re-delete entries.
        random.shuffle(keys)
        for key in keys:
            with self.assertRaises(KeyError):
                del self._hashtable[key]

    def test_len(self) -> None:
        size = 0
        self.assertEqual(size, len(self._hashtable))

        # Assert size follows addition of key, value pairs.
        keys = Array(random.sample(range(self.TEST_SIZE), self.TEST_SIZE))
        for key in keys:
            value = random.choice(range(self.TEST_SIZE))
            self._hashtable[key] = value
            size += 1
            self.assertEqual(size, len(self._hashtable))

        # Assert size doesn't change when existing keys values' are changed.
        random.shuffle(keys)
        for key in keys:
            value = random.choice(range(self.TEST_SIZE))
            self._hashtable[key] = value
            self.assertEqual(size, len(self._hashtable))

        # Assert size follows deletion of key, values pairs.
        random.shuffle(keys)
        for key in keys:
            del self._hashtable[key]
            size -= 1
            self.assertEqual(size, len(self._hashtable))

    def test_items(self) -> None:
        # Add key, value pairs.
        keys = Array(random.sample(range(self.TEST_SIZE), self.TEST_SIZE))
        pairs = Array(len(keys))
        for i, key in enumerate(keys):
            value = random.choice(range(self.TEST_SIZE))
            self._hashtable[key] = value
            pairs[i] = (key, value)

        # Assert all key, value pairs are yielded exactly once.
        visited = 0
        for key, value in self._hashtable.items():
            visited += 1
            self.assertIn((key, value), pairs)
        self.assertEqual(len(pairs), visited)

    def test_values(self) -> None:
        # Add key, value pairs.
        keys = Array(random.sample(range(self.TEST_SIZE), self.TEST_SIZE))
        values = Array(random.sample(range(self.TEST_SIZE), self.TEST_SIZE))
        for key, value in zip(keys, values):
            self._hashtable[key] = value

        # Assert all values are yielded exactly once.
        visited = 0
        for value in self._hashtable.values():
            visited += 1
            self.assertIn(value, values)
        self.assertEqual(len(values), visited)

    def test_serialise(self) -> None:
        b = pickle.dumps(self._hashtable)
        hashtable = pickle.loads(b)
        self.assertEqual(0, len(hashtable))
        for _ in hashtable:
            self.fail()
        for i in range(self.TEST_SIZE):
            self.assertNotIn(i, hashtable)

        keys = Array(random.sample(range(self.TEST_SIZE), self.TEST_SIZE))
        pairs: Array[Tuple[int, int]] = Array(len(keys))
        for i, key in enumerate(keys):
            value = random.choice(range(self.TEST_SIZE))
            self._hashtable[key] = value
            pairs[i] = (key, value)

        b = pickle.dumps(self._hashtable)
        hashtable = pickle.loads(b)
        random.shuffle(pairs)
        for key, value in pairs:
            self.assertIn(key, hashtable)
            self.assertEqual(value, hashtable[key])

    @staticmethod
    def _find(pairs: Sequence[Tuple[Any, Any]], key):
        return next(map(lambda p: p[1], filter(lambda p: p[0] == key, pairs)))
