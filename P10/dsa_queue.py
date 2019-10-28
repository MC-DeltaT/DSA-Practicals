from collections import deque
from typing import Any, Iterator


class DSAQueue:
    def __init__(self) -> None:
        self._queue = deque()

    def enqueue(self, obj: Any) -> None:
        self._queue.append(obj)

    def dequeue(self) -> Any:
        if self.is_empty():
            raise ValueError("Queue is empty.")
        return self._queue.popleft()

    def peek(self) -> Any:
        return self._queue[0]

    def is_empty(self) -> bool:
        return len(self._queue) == 0

    # For visualisation purposes only.
    def as_list(self) -> list:
        return list(self._queue)

    def __repr__(self) -> str:
        return repr(self.as_list())

    def __iter__(self) -> Iterator[Any]:
        return iter(self._queue)
