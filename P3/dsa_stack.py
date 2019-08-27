from dsa_linked_list import DSALinkedList

from typing import Any, Iterator


class DSAStack:
    def __init__(self) -> None:
        self._list = DSALinkedList()

    def push(self, obj: Any) -> None:
        self._list.insert_first(obj)

    def pop(self) -> Any:
        tmp = self.top()
        self._list.remove_first()
        return tmp

    def top(self) -> Any:
        if self.is_empty():
            raise ValueError("Stack is empty.")
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
