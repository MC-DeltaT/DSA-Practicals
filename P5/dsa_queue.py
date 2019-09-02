from dsa_linked_list import DSALinkedList

from typing import Any, Iterator


class DSAQueue:
    def __init__(self) -> None:
        self._list = DSALinkedList()

    def enqueue(self, obj: Any) -> None:
        self._list.insert_last(obj)

    def dequeue(self) -> Any:
        if self.is_empty():
            raise ValueError("Queue is empty.")
        tmp = self.peek()
        self._list.remove_first()
        return tmp

    def peek(self) -> Any:
        return self._list.peek_first()

    def is_empty(self) -> bool:
        return self._list.is_empty()

    # For visualisation purposes only.
    def as_list(self) -> list:
        return list(self._list)

    def __repr__(self) -> str:
        return repr(self.as_list())

    def __iter__(self) -> Iterator[Any]:
        return iter(self._list)
