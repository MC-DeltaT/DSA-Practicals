from .hash_table import HashTable

from typing import Generic, Hashable, Iterator, TypeVar


__all__ = [
    "Set"
]


T = TypeVar("T", bound=Hashable)


class Set(Generic[T]):
    # As this set is implemented with a hashtable, capacity indicates the initial
    # number of items able to be stored in that hashtable.
    def __init__(self, capacity: int) -> None:
        self._hashtable: HashTable[T, None] = HashTable(capacity)

    # Adds an item to the set, if it doesn't already exist.
    def add(self, item: T) -> None:
        self._hashtable[item] = None

    # Removes an item from the set if it exists, otherwise raises KeyError.
    def remove(self, item: T) -> None:
        del self._hashtable[item]

    def __len__(self) -> int:
        return len(self._hashtable)

    def __contains__(self, item: T) -> bool:
        return item in self._hashtable

    def __iter__(self) -> Iterator[T]:
        return iter(self._hashtable)
