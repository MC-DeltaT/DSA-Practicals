from . import SinglyLinkedList

from typing import Any, Iterator


__all__ = [
    "Set"
]


# Slow set implementation using linked lists.
class Set:
    def __init__(self) -> None:
        self._items = SinglyLinkedList()

    def add(self, item: Any) -> bool:
        if item in self:
            added = False
        else:
            self._items.insert_last(item)
            added = True
        return added

    def remove(self, item: Any) -> None:
        self._items.remove(item)

    def __len__(self) -> int:
        return len(self._items)

    def __contains__(self, item: Any) -> bool:
        return item in self._items

    def __iter__(self) -> Iterator[Any]:
        return iter(self._items)
