from .impl import SinglyLinkedListBase

from typing import Any, Iterable, Iterator, Optional


__all__ = [
    "SinglyLinkedList"
]


# Singly-linked, double-ended linked list.
class SinglyLinkedList:

    def __init__(self, items: Optional[Iterable] = None) -> None:
        self._base = SinglyLinkedListBase()
        if items:
            for item in items:
                self.insert_last(item)

    def insert_first(self, item: Any) -> None:
        self._base.insert_first(item)

    def insert_last(self, item: Any) -> None:
        self._base.insert_last(item)

    def peek_first(self) -> Any:
        self._raise_for_empty()
        return self._base.head.data

    def peek_last(self) -> Any:
        self._raise_for_empty()
        return self._base.tail.data

    def remove(self, item: Any) -> None:
        self._base.remove(item)

    def __len__(self) -> int:
        return self._base.size

    def __iter__(self) -> Iterator[Any]:
        return iter(self._base)

    def __repr__(self) -> str:
        return "[" + ", ".join(map(repr, self)) + "]"

    def _raise_for_empty(self) -> None:
        if len(self) == 0:
            raise ValueError("List is empty.")
