from typing import Any, Iterator


class DSALinkedList:
    class ListNode:
        def __init__(self, obj: Any, prev=None, next=None) -> None:
            self.obj = obj
            self.prev = prev
            self.next = next

    class ListIterator:
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

    class ListReverseIterator:
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

    def __init__(self) -> None:
        self._head = None
        self._tail = None

    def insert_first(self, obj: Any) -> None:
        if self.is_empty():
            self._head = self.ListNode(obj)
            self._tail = self._head
        else:
            old_head = self._head
            self._head = self.ListNode(obj, next=old_head)
            old_head.prev = self._head

    def insert_last(self, obj: Any) -> None:
        if self.is_empty():
            self.insert_first(obj)
        else:
            old_tail = self._tail
            self._tail = self.ListNode(obj, prev=old_tail)
            old_tail.next = self._tail

    def remove_first(self) -> None:
        self._raise_for_empty()
        # 1 element.
        if self._head == self._tail:
            self._head = None
            self._tail = None
        else:
            self._head = self._head.next
            self._head.prev = None

    def remove_last(self) -> None:
        # 0 or 1 elements.
        if self._head == self._tail:
            self.remove_first()
        else:
            self._tail = self._tail.prev
            self._tail.next = None

    def remove_all(self) -> None:
        self._head = None
        self._tail = None

    def peek_first(self) -> Any:
        self._raise_for_empty()
        return self._head.obj

    def peek_last(self) -> Any:
        self._raise_for_empty()
        return self._tail.obj

    def is_empty(self) -> bool:
        return self._head is None

    def _raise_for_empty(self) -> None:
        if self.is_empty():
            raise ValueError("List is empty.")

    def __iter__(self) -> Iterator[Any]:
        return self.ListIterator(self._head)

    def __reversed__(self) -> Iterator[Any]:
        return self.ListReverseIterator(self._tail)
