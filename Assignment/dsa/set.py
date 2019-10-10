from . import HashTable

from typing import Hashable, Iterator


__all__ = [
    "Set"
]


# TODO: set implementation.
class Set:
    def __init__(self, capacity: int) -> None:
        self._hashtable = HashTable(capacity)

    def add(self, item: Hashable) -> None:
        self._hashtable[item] = None

    def remove(self, item: Hashable) -> None:
        del self._hashtable[item]

    def __len__(self) -> int:
        return len(self._hashtable)

    def __contains__(self, item: Hashable) -> bool:
        return item in self._hashtable

    def __iter__(self) -> Iterator[Hashable]:
        return iter(self._hashtable)
