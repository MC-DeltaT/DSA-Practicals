# Sourced from my Data Structures & Algorithms practical worksheet 3 submission,
# with modifications.

from typing import Any, Iterable, Iterator, Optional


__all__ = [
    "DoublyLinkedList"
]


# Doubly-linked, double-ended linked list.
class DoublyLinkedList:
    class _Node:
        def __init__(self, data: Any, prev: Optional["DoublyLinkedList._Node"] = None,
                     next: Optional["DoublyLinkedList._Node"] = None) -> None:
            self.data = data
            self.prev = prev
            self.next = next

    def __init__(self, items: Optional[Iterable] = None) -> None:
        self._head: Optional["DoublyLinkedList._Node"] = None
        self._tail: Optional["DoublyLinkedList._Node"] = None
        self._size = 0
        if items:
            for item in items:
                self.insert_last(item)

    @property
    def is_empty(self) -> bool:
        return len(self) == 0

    def insert_first(self, item: Any) -> None:
        if self.is_empty:
            self._head = self._Node(item)
            self._tail = self._head
        else:
            old_head = self._head
            self._head = self._Node(item, next=old_head)
            old_head.prev = self._head
        self._size += 1

    def insert_last(self, item: Any) -> None:
        if self.is_empty:
            self.insert_first(item)
        else:
            old_tail = self._tail
            self._tail = self._Node(item, prev=old_tail)
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

    def remove(self, item: Any) -> None:
        removed = False
        node = self._head
        while node and not removed:
            if node.data == item:
                if node.prev:
                    node.prev.next = node.next
                else:
                    self._head = node.next
                if node.next:
                    node.next.prev = node.prev
                else:
                    self._tail = node.prev
                self._size -= 1
                removed = True
            else:
                node = node.next
        if not removed:
            raise ValueError(f"Item `{item}` does not exist in list.")

    def peek_first(self) -> Any:
        self._raise_for_empty()
        return self._head.data

    def peek_last(self) -> Any:
        self._raise_for_empty()
        return self._tail.data

    def copy(self) -> "DoublyLinkedList":
        return DoublyLinkedList(self)

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        node = self._head
        while node is not None:
            yield node.data
            node = node.next

    def __reversed__(self) -> Iterator[Any]:
        node = self._tail
        while node is not None:
            yield node.data
            node = node.prev

    def __repr__(self) -> str:
        return "[" + ", ".join(map(repr, self)) + "]"

    def _raise_for_empty(self) -> None:
        if self.is_empty:
            raise ValueError("List is empty.")
