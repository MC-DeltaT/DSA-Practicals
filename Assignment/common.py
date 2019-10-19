from typing import Iterable, Iterator, Sized, TypeVar
from uuid import uuid4


__all__ = [
    "SizedIterable",
    "str_hash",
    "unique_file"
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


def str_hash(s: str) -> int:
    # Very simple hash function for performance reasons.
    res = 0
    for c in s:
        res = 33 * res + ord(c)
    return res


# Returns a new file with a unique filename with the given prefix and extension.
# The file is guaranteed to not already exist.
def unique_file(prefix: str, extension: str):
    done = False
    while not done:
        file_path = f"{prefix}-{uuid4()}{extension}"
        try:
            file = open(file_path, "x")
        except FileExistsError:
            pass
        else:
            done = True
    return file
