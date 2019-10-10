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

    @property
    def is_empty(self) -> bool:
        return len(self) == 0

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

    def remove_first(self) -> None:
        self._raise_for_empty()
        self._base.remove_after(self._base.before_head)

    def remove(self, item: Any) -> None:
        self._base.remove(item)

    def remove_all(self) -> None:
        self._base.remove_all()

    def copy(self) -> "SinglyLinkedList":
        return SinglyLinkedList(self)

    def __len__(self) -> int:
        return self._base.size

    def __iter__(self) -> Iterator[Any]:
        return iter(self._base)

    def __repr__(self) -> str:
        return repr(self._base)

    def _raise_for_empty(self) -> None:
        if len(self) == 0:
            raise ValueError("List is empty.")
