from typing import Collection, Iterator, Sequence, TypeVar, Union

import numpy


__all__ = [
    "Array"
]


T = TypeVar("T")


# Simple wrapper for numpy.ndarray to make it a bit easier to use.
class Array(Sequence[T]):
    def __init__(self, size_or_data: Union[int, Collection[T]]) -> None:
        if isinstance(size_or_data, int):
            self._array = numpy.empty(size_or_data, dtype=numpy.object)
        else:
            try:
                size = len(size_or_data)
                iterator = iter(size_or_data)
            except AttributeError:
                raise TypeError("size_or_data must be int or Collection.")
            else:
                self._array = numpy.empty(size, dtype=numpy.object)
                for i, item in enumerate(iterator):
                    self._array[i] = item

    def __len__(self) -> int:
        return self._array.size

    def __getitem__(self, idx: int) -> T:
        return self._array[idx]

    def __setitem__(self, idx: int, value: T) -> None:
        self._array[idx] = value

    def __iter__(self) -> Iterator[T]:
        return iter(self._array)

    def __reversed__(self) -> Iterator[T]:
        return reversed(self._array)
