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
    return res


class DSAHashTableTest(unittest.TestCase):
    TEST_SIZE = 10

    def setUp(self) -> None:
        self._hashtable = DSAHashTable(self.TEST_SIZE)

    def test_put_get(self) -> None:
        # Add key, value pairs (unique keys).
        keys = self.unique_keys()
        d = {}
        for key in keys:
            value = random.choice(range(self.TEST_SIZE))
            self._hashtable.put(key, value)
            # Assert keys map to correct values before internal resize occurs.
            self.assertEqual(value, self._hashtable.get(key))
            d[key] = value

        # Assert keys still map to correct values after internal resize.
        random.shuffle(keys)
        for key in keys:
            self.assertEqual(d[key], self._hashtable.get(key))

        # Change some values of existing keys.
        for key in random.sample(keys, self.TEST_SIZE // 2):
            d[key] += self.TEST_SIZE
            self._hashtable.put(key, d[key])
            self.assertEqual(d[key], self._hashtable.get(key))

        # Assert keys still map to correct values after all changes.
        random.shuffle(keys)
        for key in keys:
            self.assertEqual(d[key], self._hashtable.get(key))


    @staticmethod
    def unique_keys() -> List[str]:
        keys = []
        for _ in range(DSAHashTableTest.TEST_SIZE):
            key = random_string()
            while key in keys:
                key = random_string()
            keys.append(key)
        return keys


if __name__ == '__main__':
    unittest.main()
