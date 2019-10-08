from typing import Any, Iterable, Iterator, Optional


__all__ = [
    "SinglyLinkedList"
]


# Singly-linked, double-ended linked list.
class SinglyLinkedList:
    class _Node:
        def __init__(self, data: Any, next: Optional["SinglyLinkedList._Node"]) -> None:
            self.data = data
            self.next = next

    class _Iterator:
        def __init__(self, node: "SinglyLinkedList._Node") -> None:
            self._node = node

        def __iter__(self) -> "SinglyLinkedList._Iterator":
            return self

        def __next__(self) -> Any:
            if self._node is None:
                raise StopIteration()
            tmp = self._node.data
            self._node = self._node.next
            return tmp

    def __init__(self, items: Optional[Iterable] = None) -> None:
        self._head: Optional["SinglyLinkedList._Node"] = None
        self._tail: Optional["SinglyLinkedList._Node"] = None
        self._size = 0
        if items:
            for item in items:
                self.insert_last(item)

    @property
    def is_empty(self) -> bool:
        return len(self) == 0

    def insert_first(self, item: Any) -> None:
        node = self._Node(item, self._head)
        self._head = node
        if self._size == 0:
            self._tail = node
        self._size += 1

    def insert_last(self, item: Any) -> None:
        node = self._Node(item, None)
        if self._tail:
            self._tail.next = node
        self._tail = node
        if self._size == 0:
            self._head = node
        self._size += 1

    def peek_first(self) -> Any:
        self._raise_for_empty()
        return self._head.data

    def peek_last(self) -> Any:
        self._raise_for_empty()
        return self._tail.data

    def remove(self, item: Any) -> None:
        removed = False
        prev = None
        node = self._head
        while node and not removed:
            if node.data == item:
                if prev:
                    prev.next = node.next
                else:
                    self._head = node.next
                if not node.next:
                    self._tail = prev
                self._size -= 1
                removed = True
            else:
                prev = node
                node = node.next
        if not removed:
            raise ValueError(f"Item `{item}` does not exist in list.")

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        return self._Iterator(self._head)

    def __repr__(self) -> str:
        return "[" + ", ".join(map(repr, self)) + "]"

    def _raise_for_empty(self) -> None:
        if self.is_empty:
            raise ValueError("List is empty.")
