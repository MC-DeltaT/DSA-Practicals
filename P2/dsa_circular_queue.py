from dsa_queue import DSAQueue


class DSACircularQueue(DSAQueue):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._front = 0
        self._back = -1

    def enqueue(self, obj: object) -> None:
        if self.is_full():
            raise ValueError("Queue is full.")
        self._back = (self._back + 1) % len(self._array)
        self._array[self._back] = obj
        self._size += 1

    def dequeue(self) -> object:
        tmp = self.peek()
        self._front = (self._front + 1) % len(self._array)
        self._size -= 1
        return tmp

    def peek(self) -> object:
        if self.is_empty():
            raise ValueError("Queue is empty.")
        return self._array[self._front]

    # For visualisation purposes only.
    def as_list(self) -> list:
        l = []
        pos = self._front
        for i in range(self.get_size()):
            l.append(self._array[pos])
            pos = (pos + 1) % len(self._array)
        return l
