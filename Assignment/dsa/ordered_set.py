from .set import Set
from .singly_linked_list import SinglyLinkedList

from typing import Generic, Hashable, Iterator, TypeVar


__all__ = [
    "OrderedSet"
]


T = TypeVar("T", bound=Hashable)


# Linked-list/set hybrid container providing:
#   O(1) insertion.
#   O(n) deletion.
#   O(1) containment check.
#   Iteration in insertion order.
class OrderedSet(Generic[T]):
    # As this set is implemented with a hashtable, capacity indicates the initial
    # number of items able to be stored in that hashtable.
    def __init__(self, capacity: int) -> None:
        self._list: SinglyLinkedList[T] = SinglyLinkedList()
        self._set: Set[T] = Set(capacity)

    # Adds an item to the start of the container if it doesn't already exist
    # Returns a bool indicating whether the item was added or not.
    def add_first(self, item: T) -> bool:
        if item in self:
            added = False
        else:
            self._list.insert_first(item)
            self._set.add(item)
            added = True
        return added

    # Adds an item to the end of the container if it doesn't already exist.
    # Returns a bool indicating whether the item was added or not.
    def add_last(self, item: T) -> bool:
        added = self._set.add(item)
        if added:
            self._list.insert_last(item)
        return added

    def remove(self, item: T) -> None:
        self._list.remove(item)
        self._set.remove(item)

    def __len__(self) -> int:
        return len(self._set)

    def __contains__(self, item: T) -> bool:
        return item in self._set

    def __iter__(self) -> Iterator[T]:
        return iter(self._list)

    def __repr__(self) -> str:
        return "{" + ", ".join(map(repr, self)) + "}"

