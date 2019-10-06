# Sourced from my Data Structures & Algorithms practical worksheet 3 submission,
# with modifications.

from typing import Any, Iterable, Iterator, Optional


__all__ = [
    "LinkedList"
]


class LinkedList:
    class _ListNode:
        def __init__(self, obj: Any, prev=None, next=None) -> None:
            self.obj = obj
            self.prev = prev
            self.next = next

    class _ListIterator:
        def __init__(self, node) -> None:
            self._node = node

        def __iter__(self):
            return self

        def __next__(self) -> Any:
            if self._node is None:
                raise StopIteration()
            tmp = self._node.obj
            self._node = self._node.next
            return tmp

    class _ListReverseIterator:
        def __init__(self, node) -> None:
            self._node = node

        def __iter__(self):
            return self

        def __next__(self) -> Any:
            if self._node is None:
                raise StopIteration()
            tmp = self._node.obj
            self._node = self._node.prev
            return tmp

    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        self._head = None
        self._tail = None
        self._size = 0
        if iterable:
            for e in iterable:
                self.insert_last(e)

    @property
    def is_empty(self) -> bool:
        return len(self) == 0

    def insert_first(self, obj: Any) -> None:
        if self.is_empty:
            self._head = self._ListNode(obj)
            self._tail = self._head
        else:
            old_head = self._head
            self._head = self._ListNode(obj, next=old_head)
            old_head.prev = self._head
        self._size += 1

    def insert_last(self, obj: Any) -> None:
        if self.is_empty:
            self.insert_first(obj)
        else:
            old_tail = self._tail
            self._tail = self._ListNode(obj, prev=old_tail)
            old_tail.next = self._tail
            self._size += 1

    def remove_first(self) -> None:
        self._raise_for_empty()
        if len(self) == 1:
            self._head = None
            self._tail = None
        else:
            self._head = self._head.next
            self._head.prev = None
        self._size -= 1

    def remove_last(self) -> None:
        if len(self) <= 1:
            self.remove_first()
        else:
            self._tail = self._tail.prev
            self._tail.next = None
            self._size -= 1

    def remove_all(self) -> None:
        self._head = None
        self._tail = None
        self._size = 0

    def peek_first(self) -> Any:
        self._raise_for_empty()
        return self._head.obj

    def peek_last(self) -> Any:
        self._raise_for_empty()
        return self._tail.obj

    def copy(self):
        return LinkedList(self)

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        return self._ListIterator(self._head)

    def __reversed__(self) -> Iterator[Any]:
        return self._ListReverseIterator(self._tail)

    def __contains__(self, item: Any) -> bool:
        return any(map(lambda e: e == item, self))

    def _raise_for_empty(self) -> None:
        if self.is_empty:
            raise ValueError("List is empty.")
