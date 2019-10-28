from dsa_hash_table import DSAHashTable

import random
from typing import List
import unittest


class DSAHashTableTest(unittest.TestCase):
    TEST_SIZE = 10000

    def setUp(self) -> None:
        self._hashtable = DSAHashTable()

    def test_put_get_has(self) -> None:
        keys = self._unique_keys(self.TEST_SIZE)

        # Assert nothing in table yet.
        for key in keys:
            with self.assertRaises(KeyError):
                self._hashtable.get(key)
            self.assertFalse(self._hashtable.has(key))

        # Assert key, value pairs are correct before any internal resize occurs.
        d = {}
        for key in keys:
            value = random.choice(range(self.TEST_SIZE))
            self._hashtable.put(key, value)
            self.assertEqual(value, self._hashtable.get(key))
            self.assertTrue(self._hashtable.has(key))
            d[key] = value

        # Assert key, values pairs are correct after internal resize.
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
        keys = self._unique_keys(self.TEST_SIZE)

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

    def test_size(self) -> None:
        size = 0
        self.assertEqual(size, self._hashtable.size)

        # Assert size follows addition of key, value pairs.
        keys = self._unique_keys(self.TEST_SIZE)
        for key in keys:
            value = random.choice(range(self.TEST_SIZE))
            self._hashtable.put(key, value)
            size += 1
            self.assertEqual(size, self._hashtable.size)

        # Assert size doesn't change when existing keys values' are changed.
        random.shuffle(keys)
        for key in keys:
            value = random.choice(range(self.TEST_SIZE))
            self._hashtable.put(key, value)
            self.assertEqual(size, self._hashtable.size)

        # Assert size follows deletion of key, values pairs.
        random.shuffle(keys)
        for key in keys:
            self._hashtable.delete(key)
            size -= 1
            self.assertEqual(size, self._hashtable.size)

    def test_items(self) -> None:
        # Add key, value pairs.
        pairs = set()
        for key in self._unique_keys(self.TEST_SIZE):
            value = random.choice(range(self.TEST_SIZE))
            self._hashtable.put(key, value)
            pairs.add((key, value))

        # Assert all key, value pairs are yielded exactly once.
        actual = set(self._hashtable.items())
        self.assertSetEqual(pairs, actual)

    @staticmethod
    def _unique_keys(count: int) -> List[str]:
        def random_string(max_size: int = 20) -> str:
            size = random.randint(1, max_size)
            res = ""
            for i in range(size):
                # Random Unicode character.
                res += chr(random.randint(0, 1114111))
            assert 0 < len(res) <= max_size
            return res

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
    unittest.main(verbosity=2)
