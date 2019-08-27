from dsa_queue import DSAQueue


class DSAShufflingQueue(DSAQueue):
    def enqueue(self, obj: object) -> None:
        if self.is_full():
            raise ValueError("Queue is full.")
        self._array[self._size] = obj
        self._size += 1

    def dequeue(self) -> object:
        tmp = self.peek()
        for i in range(0, self._size - 1):
            self._array[i] = self._array[i + 1]
        self._size -= 1
        return tmp

    def peek(self) -> object:
        if self.is_empty():
            raise ValueError("Queue is empty.")
        return self._array[0]

    # For visualisation purposes only.
    def as_list(self) -> list:
        return list(self._array[:self.get_size()])
