from typing import Any, Iterator, Tuple


__all__ = [
    'DSAHashTable'
]


class DSAHashTable:
    def __init__(self) -> None:
        self._dict = {}

    # Adds the key, value pair to the hashtable, or if the key already exists, updates the value.
    def put(self, key: str, value: Any) -> None:
        self._dict[key] = value

    # Gets the value with the given key, or raises KeyError if there is no such key.
    def get(self, key: str) -> Any:
        return self._dict[key]

    # Deletes the key, value pair with the given key, or raises KeyError if there is no such key.
    def delete(self, key: str) -> None:
        del self._dict[key]

    def has(self, key: str) -> bool:
        return key in self._dict

    # The number of key, value pairs currently stored.
    @property
    def size(self) -> int:
        return len(self._dict)

    # Returns an iterator of all key, value pairs.
    def items(self) -> Iterator[Tuple[str, Any]]:
        return self._dict.items()
