import numpy


class DSAStack:
    def __init__(self, max_size: int) -> None:
        if max_size <= 0:
            raise ValueError("max_size must be > 0.")
        self._array = numpy.empty(max_size, dtype=object)
        self._size = 0

    def push(self, obj: object) -> None:
        if self.is_full():
            raise ValueError("Stack is full.")
        self._array[self._size] = obj
        self._size += 1

    def pop(self) -> object:
        tmp = self.top()
        self._size -= 1
        return tmp

    def top(self) -> object:
        if self.is_empty():
            raise ValueError("Stack is empty.")
        return self._array[self._size - 1]

    def is_empty(self) -> bool:
        return self._size == 0

    def is_full(self) -> bool:
        return self._size == self._array.size

    def get_size(self) -> int:
        return self._size

    # For visualisation purposes only.
    def as_list(self) -> list:
        return list(reversed(self._array[:self.get_size()]))

    def __repr__(self) -> str:
        return repr(self.as_list())
