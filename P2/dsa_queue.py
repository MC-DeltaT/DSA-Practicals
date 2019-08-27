from abc import ABC, abstractmethod

import numpy


class DSAQueue(ABC):
    def __init__(self, max_size: int) -> None:
        if max_size <= 0:
            raise ValueError("max_size must be > 0.")
        self._array = numpy.empty(max_size, dtype=object)
        self._size = 0

    @abstractmethod
    def enqueue(self, obj: object) -> None:
        pass

    @abstractmethod
    def dequeue(self) -> object:
        pass

    @abstractmethod
    def peek(self) -> object:
        pass

    def is_empty(self) -> bool:
        return self._size == 0

    def is_full(self) -> bool:
        return self._size == len(self._array)

    def get_size(self) -> int:
        return self._size

    # For visualisation purposes only.
    @abstractmethod
    def as_list(self) -> list:
        pass

    def __repr__(self) -> str:
        return repr(self.as_list())
