from typing import Any, Iterable, Iterator, Optional


__all__ = [
    "SinglyLinkedListBase"
]


# Provides the base for a singly-linked, double-ended linked list.
# Exposes internals so they can be reused across multiple data structures.
# (Not meant to be used as a public interface.)
class SinglyLinkedListBase:
    class Node:
        def __init__(self, data: Any, next: Optional["SinglyLinkedListBase.Node"]) -> None:
            self.data = data
            self.next = next

    def __init__(self, items: Optional[Iterable] = None) -> None:
        # Use of "before head" node allows uniform removal of nodes anywhere in list.
        self.before_head = self.Node(None, None)
        self.head: Optional["SinglyLinkedListBase.Node"] = None
        self.tail = self.before_head
        self.size = 0
        if items:
            for item in items:
                self.insert_last(item)

    def insert_first(self, item: Any) -> None:
        node = self.Node(item, self.head)
        self.before_head.next = node
        self.head = node
        if self.size == 0:
            self.tail = node
        self.size += 1

    def insert_last(self, item: Any) -> None:
        node = self.Node(item, None)
        self.tail.next = node
        self.tail = node
        self.head = self.before_head.next
        self.size += 1

    def find(self, item: Any) -> "SinglyLinkedListBase.Node":
        found = False
        node = self.head
        while node and not found:
            if node.data == item:
                found = True
        if not found:
            raise ValueError(f"Item `{item}` does not exist in list.")
        return node

    def remove(self, item: Any) -> None:
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

    def remove_after(self, node: "SinglyLinkedListBase.Node") -> None:
        prev = node
        node = prev.next
        prev.next = node.next
        if node.next is None:
            self.tail = prev
        self.size -= 1

    def __iter__(self) -> Iterator[Any]:
        node = self.head
        while node is not None:
            yield node.data
            node = node.next

    def __repr__(self) -> str:
        return "[" + ", ".join(map(repr, self)) + "]"

    def _raise_for_empty(self) -> None:
        if self.size == 0:
            raise ValueError("List is empty.")
