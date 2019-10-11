from .impl import SinglyLinkedListBase

from typing import Collection, Iterable, Iterator, Optional, TypeVar


__all__ = [
    "SinglyLinkedList"
]


T = TypeVar("T")


# Singly-linked, double-ended linked list.
class SinglyLinkedList(Collection[T]):
    def __init__(self, items: Optional[Iterable[T]] = None) -> None:
        self._base: SinglyLinkedListBase[T] = SinglyLinkedListBase()
        if items:
            for item in items:
                self.insert_last(item)

    @property
    def is_empty(self) -> bool:
        return len(self) == 0

    def insert_first(self, item: T) -> None:
        self._base.insert_first(item)

    def insert_last(self, item: T) -> None:
        self._base.insert_last(item)

    def peek_first(self) -> T:
        self._raise_for_empty()
        return self._base.head.data

    def peek_last(self) -> T:
        self._raise_for_empty()
        return self._base.tail.data

    def remove_first(self) -> None:
        self._raise_for_empty()
        self._base.remove_after(self._base.before_head)

    def remove(self, item: T) -> None:
        self._base.remove(item)

    def remove_all(self) -> None:
        self._base.remove_all()

    def copy(self) -> "SinglyLinkedList[T]":
        return SinglyLinkedList(self)

    def __len__(self) -> int:
        return self._base.size

    def __iter__(self) -> Iterator[T]:
        return iter(self._base)

    # Only for Collection requirement.
    def __contains__(self, item: T) -> bool:
        return item in iter(self)

    def __repr__(self) -> str:
        return repr(self._base)

    def _raise_for_empty(self) -> None:
        if len(self) == 0:
            raise ValueError("List is empty.")
