from typing import Generic, Iterator, Optional, TypeVar


__all__ = [
    "SinglyLinkedListBase"
]


T = TypeVar("T")

# Provides the base for a singly-linked, double-ended linked list.
# Exposes internals so they can be reused across multiple data structures.
# (Not meant to be used as a public interface.)
class SinglyLinkedListBase(Generic[T]):
    class Node(Generic[T]):
        def __init__(self, data: T, next: Optional["SinglyLinkedListBase.Node[T]"]) -> None:
            self.data = data
            self.next = next

    def __init__(self) -> None:
        # Use of "before head" node allows uniform removal of nodes anywhere in list.
        self.before_head: "SinglyLinkedListBase.Node[T]" = self.Node(None, None)
        # Pointing tail to "before head" when list is empty simplifies certain operations.
        self.tail: "SinglyLinkedListBase.Node[T]" = self.before_head
        self.size = 0

    @property
    def head(self) -> "SinglyLinkedListBase.Node[T]":
        return self.before_head.next

    def insert_first(self, item: T) -> None:
        node = self.Node(item, self.head)
        self.before_head.next = node
        if self.size == 0:
            self.tail = node
        self.size += 1

    def insert_last(self, item: T) -> None:
        node = self.Node(item, None)
        self.tail.next = node
        self.tail = node
        self.size += 1

    def find(self, item: T) -> "SinglyLinkedListBase.Node[T]":
        found = False
        node = self.head
        while node and not found:
            if node.data == item:
                found = True
            else:
                node = node.next
        if not found:
            raise ValueError(f"Item `{item}` does not exist in list.")
        return node

    def remove_after(self, node: "SinglyLinkedListBase.Node[T]") -> None:
        if node.next is None:
            raise ValueError("Node has no next node.")
        prev = node
        node = prev.next
        prev.next = node.next
        if node.next is None:
            # Removed last node.
            self.tail = prev
        self.size -= 1

    def remove(self, item: T) -> None:
        removed = False
        prev = self.before_head
        node = self.head
        while node and not removed:
            if node.data == item:
                self.remove_after(prev)
                removed = True
            else:
                prev = node
                node = node.next
        if not removed:
            raise ValueError(f"Item `{item}` does not exist in list.")

    def remove_all(self) -> None:
        self.before_head.next = None
        self.tail = self.before_head
        self.size = 0

    def __iter__(self) -> Iterator[T]:
        node = self.head
        while node is not None:
            yield node.data
            node = node.next

    def __repr__(self) -> str:
        return "[" + ", ".join(map(repr, self)) + "]"
