from typing import Collection, Generic, Iterable, Iterator, Optional, TypeVar


__all__ = [
    "SinglyLinkedList"
]


T = TypeVar("T")


# Singly-linked, double-ended linked list.
class SinglyLinkedList(Collection[T]):
    class _Node(Generic[T]):
        # Lots of linked list traversal, easy optimisation here.
        __slots__ = ("data", "next")

        def __init__(self, data: T, next: Optional["SinglyLinkedList._Node[T]"]) -> None:
            self.data = data
            self.next = next

    __slots__ = ("_before_head", "_head", "_size", "_tail")

    def __init__(self, data: Optional[Iterable] = None) -> None:
        # Use of "before head" node allows uniform removal of nodes anywhere in list.
        self._before_head: "SinglyLinkedList._Node[T]" = self._Node(None, None)
        self._head: Optional["SinglyLinkedList._Node[T]"] = None
        # Pointing tail to "before head" when list is empty simplifies certain operations.
        self._tail: "SinglyLinkedList._Node[T]" = self._before_head
        self._size = 0

        if data:
            for item in data:
                self.insert_last(item)

    def peek_first(self) -> T:
        self._raise_for_empty()
        return self._head.data

    def peek_last(self) -> T:
        self._raise_for_empty()
        return self._tail.data

    def insert_first(self, item: T) -> None:
        node = self._Node(item, self._head)
        self._before_head.next = node
        self._head = node
        if self._size == 0:
            self._tail = node
        self._size += 1

    def insert_last(self, item: T) -> None:
        node = self._Node(item, None)
        self._tail.next = node
        self._tail = node
        self._head = self._before_head.next
        self._size += 1

    def remove_first(self) -> None:
        self._raise_for_empty()
        self._remove_after(self._before_head)

    # Removes the first element that compares equal to item.
    def remove(self, item: T) -> None:
        removed = False
        prev = self._before_head
        node = self._head
        while node and not removed:
            if node.data == item:
                self._remove_after(prev)
                removed = True
            else:
                prev = node
                node = node.next
        if not removed:
            raise ValueError(f"Item `{item}` does not exist in list.")

    def remove_all(self) -> None:
        self._before_head.next = None
        self._head = None
        self._tail = self._before_head
        self._size = 0

    def copy(self) -> "SinglyLinkedList[T]":
        return SinglyLinkedList(self)

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        node = self._head
        while node is not None:
            yield node.data
            node = node.next

    def __contains__(self, item: T) -> bool:
        # Must be implemented to satisfy Collection.

        return item in iter(self)

    def __repr__(self) -> str:
        return "[" + ", ".join(map(repr, self)) + "]"

    # Removes the node after the given node.
    # (Can't remove node from itself in singly-linked, because can't access previous node.)
    def _remove_after(self, node: "SinglyLinkedList._Node[T]") -> None:
        assert node.next is not None
        prev = node
        node = prev.next
        prev.next = node.next
        if node.next is None:
            # Removed last node.
            self._tail = prev
        self._head = self._before_head.next
        self._size -= 1

    def _raise_for_empty(self) -> None:
        if len(self) == 0:
            raise ValueError("List is empty.")
