from .array import Array
from .singly_linked_list import SinglyLinkedList
from common import str_hash

from itertools import chain, takewhile
from math import ceil, floor
from typing import Generic, Hashable, Iterator, Optional, Tuple, TypeVar


__all__ = [
    "HashTable"
]


K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class HashTable(Generic[K, V]):
    class _Entry(Generic[K, V]):
        def __init__(self, key: K, value: V) -> None:
            self.key = key
            self.value = value

        def __eq__(self, key: K) -> bool:
            return key == self.key

        # For debugging purposes only.
        def __repr__(self) -> str:
            return f"{self.key}: {self.value}"

    # Initialises the hashtable with the given starting capacity and load factor.
    # capacity defaults to 100 and must be >= 1 if provided.
    # load_factor defaults to max_load_factor and must be >0 if provided.
    # min_load_factor: on item removal, load factors <= this amount trigger the capacity to be reduced.
    # max_load_factor: on item insertion, load factors >= this amount trigger the capacity to be increased.
    # shrink_factor: fraction decrease in capacity when a capacity reduction is triggered.
    #                (Unless the resulting capacity would be too small to fit all items.)
    # growth_factor: fraction increase in capacity when a capacity increase is triggered.
    def __init__(self, capacity: Optional[int] = None, load_factor: Optional[float] = None,
                 min_load_factor: Optional[float] = None, max_load_factor: Optional[float] = None,
                 shrink_factor: Optional[float] = None, growth_factor: Optional[float] = None) -> None:
        if capacity is None:
            capacity = 100
        if capacity < 1:
            raise ValueError(f"capacity must be >=1, got {capacity}.")
        if min_load_factor is None:
            min_load_factor = 0.5
        if min_load_factor < 0:
            raise ValueError(f"min_load_factor must be >=0, got {min_load_factor}.")
        if max_load_factor is None:
            max_load_factor = 2
        if max_load_factor <= 0:
            raise ValueError(f"max_load_factor must be >0, got {max_load_factor}.")
        if shrink_factor is None:
            shrink_factor = 0.25
        if not 0 <= shrink_factor < 1:
            raise ValueError(f"shrink_factor must be >=0 and <1, got {shrink_factor}.")
        if growth_factor is None:
            growth_factor = 0.5
        if growth_factor < 0:
            raise ValueError(f"growth_factor must be >=0, got {growth_factor}.")
        if load_factor is None:
            load_factor = max_load_factor
        if load_factor <= 0:
            raise ValueError(f"load_factor must be >0, got {load_factor}.")
        self._min_load_factor = min_load_factor
        self._max_load_factor = max_load_factor
        self._shrink_factor = shrink_factor
        self._growth_factor = growth_factor
        capacity = max(1, round(capacity / load_factor))
        self._array: Array[SinglyLinkedList["HashTable._Entry[K, V]"]] = Array(capacity)
        for i in range(capacity):
            self._array[i] = SinglyLinkedList()
        self._size = 0

    @property
    def load_factor(self) -> float:
        return len(self) / self._capacity

    # Returns an iterator of all key, value pairs.
    def items(self) -> Iterator[Tuple[K, V]]:
        return map(lambda entry: (entry.key, entry.value), chain.from_iterable(self._array))

    # Iterates over all values.
    def values(self) -> Iterator[V]:
        return map(lambda entry: entry.value, chain.from_iterable(self._array))

    # Adds the key, value pair to the hashtable, or if the key already exists, updates the value.
    # Returns a bool indicating if the key was new.
    def set(self, key: K, value: V) -> bool:
        res = self._put(key, value)
        if self.load_factor >= self._max_load_factor:
            self._increase_capacity()
        return res

    def __len__(self) -> int:
        return self._size

    # Gets the value with the given key, or raises KeyError if there is no such key.
    def __getitem__(self, key: K) -> V:
        return self._get(key).value

    # Adds the key, value pair to the hashtable, or if the key already exists, updates the value.
    def __setitem__(self, key: K, value: V) -> None:
        self.set(key, value)

    # Deletes the key, value pair with the given key, or raises KeyError if there is no such key.
    def __delitem__(self, key: K) -> None:
        chain = self._array[self._hash(key, self._capacity)]
        try:
            chain.remove(key)
        except ValueError:
            raise KeyError(f"Key `{key}` not in hash table.")
        else:
            self._size -= 1
            if self.load_factor <= self._min_load_factor:
                self._decrease_capacity()

    def __contains__(self, key: K) -> bool:
        try:
            _ = self[key]
        except KeyError:
            res = False
        else:
            res = True
        return res

    # Iterates the keys stored.
    def __iter__(self) -> Iterator[K]:
        return map(lambda entry: entry.key, chain.from_iterable(self._array))

    def __repr__(self) -> str:
        return "{" + ", ".join(map(lambda p: f"{p[0]}: {p[1]}", self.items())) + "}"

    @property
    def _capacity(self) -> int:
        return len(self._array)

    # Gets the entry object with the given key, or raises KeyError if there is no such key.
    def _get(self, key: K) -> _Entry[K, V]:
        chain = self._array[self._hash(key, self._capacity)]
        found = False
        for entry in takewhile(lambda _: not found, chain):
            if entry.key == key:
                found = True
        if not found:
            raise KeyError(f"Key `{key}` not in hash table.")
        return entry

    # Inserts a key, value pair into the array, or updates an existing key's value.
    # If the key is new, increments _size and returns True.
    def _put(self, key: K, value: V) -> bool:
        chain = self._array[self._hash(key, self._capacity)]
        exists = False
        for entry in chain:
            if entry.key == key:
                entry.value = value
                exists = True
        if not exists:
            chain.insert_last(self._Entry(key, value))
            self._size += 1
        return not exists

    # Increases the capacity by at least the amount specified by _growth_factor.
    def _increase_capacity(self) -> None:
        assert self._capacity > 0
        assert self._growth_factor >= 0
        new_capacity = ceil(self._capacity * (1.0 + self._growth_factor))
        self._set_capacity(new_capacity)

    # Decreases the capacity by the amount specified by _shrink_factor, if possible.
    def _decrease_capacity(self) -> None:
        assert 0 <= self._shrink_factor < 1
        new_capacity = floor(self._capacity * (1.0 - self._shrink_factor))
        new_capacity = max(new_capacity, 1)
        self._set_capacity(new_capacity)

    # Resizes the current array and rehashes all key, value pairs back into it.
    def _set_capacity(self, new_capacity: int) -> None:
        old_array = self._array
        self._array = Array(new_capacity)
        self._size = 0
        for i in range(new_capacity):
            self._array[i] = SinglyLinkedList()
        for chain in old_array:
            for entry in chain:
                self._put(entry.key, entry.value)

    def _hash(self, key: Hashable, array_size: int) -> int:
        # Use custom hash function for strings (to show that I can implement a hash function),
        # but otherwise use built-in hash so we don't unnecessarily restrict the hash table to only strings.
        # (Unrealistic to re-implement hash functions for every possible Python type.)
        if isinstance(key, str):
            hasher = str_hash
        else:
            hasher = hash
        return hasher(key) % array_size
