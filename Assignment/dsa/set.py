from . import HashTable

from typing import Hashable, Iterator


__all__ = [
    "Set"
]


class Set:
    # As this set is implemented with a hashtable, capacity indicates the initial
    # number of items able to be stored in that hashtable.
    def __init__(self, capacity: int) -> None:
        self._hashtable = HashTable(capacity)

    # Adds an item to the set, if it doesn't already exist.
    def add(self, item: Hashable) -> None:
        self._hashtable[item] = None

    # Removes an item from the set if it exists, otherwise raises KeyError.
    def remove(self, item: Hashable) -> None:
        del self._hashtable[item]

    def __len__(self) -> int:
        return len(self._hashtable)

    def __contains__(self, item: Hashable) -> bool:
        return item in self._hashtable

    def __iter__(self) -> Iterator[Hashable]:
        return iter(self._hashtable)
