from . import HashTable
from .impl import SinglyLinkedListBase

from typing import Hashable, Iterator


__all__ = [
    "OrderedSet"
]


# Linked-list/set hybrid container providing:
#   O(1) insertion.
#   O(1) deletion.
#   O(1) containment check.
#   Iteration in insertion order.
class OrderedSet:
    def __init__(self, capacity: int) -> None:
        self._list = SinglyLinkedListBase()
        self._hashtable = HashTable(capacity)

    # Adds an item to the start of the container if it isn't already present.
    # Returns a bool indicating whether the item was added or not.
    def add_first(self, item: Hashable) -> bool:
        if item in self:
            added = False
        else:
            self._list.insert_first(item)
            self._hashtable[item] = self._list.before_head
            added = True
        return added

    # Adds an item to the end of the container if it isn't already present.
    # Returns a bool indicating whether the item was added or not.
    def add_last(self, item: Hashable) -> bool:
        if item in self:
            added = False
        else:
            prev = self._list.tail
            self._list.insert_last(item)
            self._hashtable[item] = prev
            added = True
        return added

    def remove(self, item: Hashable) -> None:
        prev = self._hashtable[item]
        self._list.remove_after(prev)
        del self._hashtable[item]

    def __len__(self) -> int:
        return self._list.size

    def __contains__(self, item: Hashable) -> bool:
        return item in self._hashtable

    def __iter__(self) -> Iterator[Hashable]:
        return iter(self._list)

    def __repr__(self) -> str:
        return "{" + ", ".join(map(repr, self)) + "}"

