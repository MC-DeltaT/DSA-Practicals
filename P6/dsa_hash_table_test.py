from dsa_hash_table import DSAHashTable

import random
from typing import List
import unittest


def random_string(max_size: int = 20) -> str:
    size = random.randint(1, max_size)
    res = ""
    for i in range(size):
        # Random Unicode character.
        res += chr(random.randint(0, 1114111))
    assert 0 < len(res) <= max_size
    return res


class DSAHashTableTest(unittest.TestCase):
    TEST_SIZE = 10000

    def setUp(self) -> None:
        self._hashtable = DSAHashTable(self.TEST_SIZE)

    def test_next_prime(self) -> None:
        # Assert next prime from non-prime is correct.
        for x, y in [(1, 2), (4, 5), (6, 7), (8, 11), (9, 11), (10, 11), (12, 13), (14, 17), (15, 17), (16, 17), (18, 19)]:
            self.assertEqual(y, DSAHashTable._next_prime(x))

        # Assert next prime from prime is correct.
        for x, y in [(2, 3), (3, 5), (5, 7), (7, 11), (11, 13), (13, 17), (17, 19)]:
            self.assertEqual(y, DSAHashTable._next_prime(x))

        # Assert out-of-range numbers are handled correctly.
        for x in range(-20, 2):
            self.assertEqual(2, DSAHashTable._next_prime(x))

    def test_prev_prime(self) -> None:
        # Assert previous prime from non-prime is correct.
        for x, y in [(4, 3), (6, 5), (8, 7), (9, 7), (10, 7), (12, 11), (14, 13), (15, 13), (16, 13), (18, 17), (19, 17)]:
            self.assertEqual(y, DSAHashTable._prev_prime(x))

        # Assert previous prime from prime is correct.
        for x, y in [(2, 2), (3, 2), (5, 3), (7, 5), (11, 7), (13, 11), (17, 13), (19, 17)]:
            self.assertEqual(y, DSAHashTable._prev_prime(x))

        # Assert out-of-range numbers are handled correctly.
        for x in range(-20, 2):
            self.assertEqual(2, DSAHashTable._next_prime(x))

    def test_put_get_has(self) -> None:
        keys = self.unique_keys(self.TEST_SIZE)

        # Assert nothing in table yet.
        for key in keys:
            with self.assertRaises(KeyError):
                self._hashtable.get(key)
            self.assertFalse(self._hashtable.has(key))

        # Add key, value pairs.
        d = {}
        for key in keys:
            value = random.choice(range(self.TEST_SIZE))
            self._hashtable.put(key, value)
            # Assert keys map to correct values before any internal resize occurs.
            self.assertEqual(value, self._hashtable.get(key))
            self.assertTrue(self._hashtable.has(key))
            d[key] = value

        # Assert keys still map to correct values after internal resize.
        random.shuffle(keys)
        for key in keys:
            self.assertEqual(d[key], self._hashtable.get(key))
            self.assertTrue(self._hashtable.has(key))

        # Change some values of existing keys.
        for key in random.sample(keys, self.TEST_SIZE // 2):
            d[key] += self.TEST_SIZE
            self._hashtable.put(key, d[key])
            self.assertEqual(d[key], self._hashtable.get(key))
            self.assertTrue(self._hashtable.has(key))

        # Assert keys still map to correct values after all changes.
        random.shuffle(keys)
        for key in keys:
            self.assertEqual(d[key], self._hashtable.get(key))
            self.assertTrue(self._hashtable.has(key))

    def test_delete(self) -> None:
        keys = self.unique_keys(self.TEST_SIZE)

        # Assert can't delete non-existent keys.
        for key in keys:
            with self.assertRaises(KeyError):
                self._hashtable.delete(key)

        # Add key, value pairs.
        for key in keys:
            value = random.choice(range(self.TEST_SIZE))
            self._hashtable.put(key, value)

        # Delete entries and assert they got removed.
        random.shuffle(keys)
        for key in keys:
            self._hashtable.delete(key)
            self.assertFalse(self._hashtable.has(key))
            with self.assertRaises(KeyError):
                self._hashtable.get(key)

        # Assert entries stayed removed after internal resize occurs.
        random.shuffle(keys)
        for key in keys:
            self.assertFalse(self._hashtable.has(key))
            with self.assertRaises(KeyError):
                self._hashtable.get(key)

        # Assert can't re-delete entries.
        random.shuffle(keys)
        for key in keys:
            with self.assertRaises(KeyError):
                self._hashtable.delete(key)

    @staticmethod
    def unique_keys(count: int) -> List[str]:
        key_set = set()
        keys = []
        for _ in range(count):
            key = random_string()
            while key in key_set:
                key = random_string()
            keys.append(key)
            key_set.add(key)
        assert len(keys) == count
        return keys


if __name__ == "__main__":
    unittest.main()
