from typing import Iterable, Iterator, Sized, TypeVar


__all__ = [
    "SizedIterable"
]


T = TypeVar("T")


class SizedIterable(Iterable[T], Sized):
    def __init__(self, iterable: Iterable[T], size: int) -> None:
        self._iterable = iterable
        self._size = size

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        return iter(self._iterable)
