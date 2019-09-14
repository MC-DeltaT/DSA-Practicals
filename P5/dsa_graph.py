from dsa_linked_list import DSALinkedList
from dsa_queue import DSAQueue
from dsa_stack import DSAStack

from typing import Any, Iterator, Optional


__all__ = [
    "DSAGraph",
    "DSAGraphVertex"
]


class DSAGraphVertex:
    def __init__(self, label: Any, value: Optional[Any] = None) -> None:
        self.label: Any = label
        self.value: Any = value
        self._adjacent: DSALinkedList = DSALinkedList()
        self.visited: bool = False

    def add_adjacent(self, vertex) -> None:
        if self.is_adjacent(vertex):
            raise ValueError(
                "Vertex labelled `{}` already has an adjacent vertex labelled `{}`."
                    .format(self.label, vertex.label))
        self._adjacent.insert_last(vertex)

    def is_adjacent(self, vertex) -> bool:
        return vertex in self._adjacent

    @property
    def adjacent(self) -> DSALinkedList:
        return self._adjacent.copy()

    def __str__(self) -> str:
        res = str(self.label)
        if self.value is not None:
            res = res + " value={}".format(self.value)
        return res

    def __repr__(self) -> str:
        return "DSAGraphVertex(label={}, value={})".format(self.label, self.value)


class DSAGraph:
    def __init__(self) -> None:
        self._vertices: DSALinkedList = DSALinkedList()

    def add_vertex(self, label: Any, value: Optional[Any] = None) -> None:
        if self.has_vertex(label):
            raise ValueError(
                "Vertex labelled `{}` already exists in graph.".format(label))
        self._vertices.insert_last(DSAGraphVertex(label, value))

    def has_vertex(self, label: Any) -> bool:
        return label in map(lambda v: v.label, self._vertices)

    def get_vertex(self, label: Any) -> DSAGraphVertex:
        try:
            return next(filter(lambda v: v.label == label, self._vertices))
        except StopIteration:
            raise ValueError(
                "Vertex labelled `{}` does not exist in graph.".format(label))

    def add_edge(self, label1: Any, label2: Any) -> None:
        vertex1 = self.get_vertex(label1)
        vertex2 = self.get_vertex(label2)
        vertex1.add_adjacent(vertex2)

    def get_adjacent(self, label: Any) -> DSALinkedList:
        return self.get_vertex(label).adjacent

    def is_adjacent(self, label1: Any, label2: Any) -> bool:
        return self.get_vertex(label1).is_adjacent(self.get_vertex(label2))

    @property
    def vertex_count(self) -> int:
        return len(self._vertices)

    @property
    def edge_count(self) -> int:
        return sum(len(v.adjacent) for v in self._vertices)

    def display_as_list(self) -> None:
        if self.vertex_count == 0:
            print("<empty graph>")
        else:
            for v1 in self._vertices:
                print("{} : ".format(v1.label), end="")
                print(", ".join(map(lambda v: str(v.label), v1.adjacent)))

    def display_as_matrix(self) -> None:
        if self.vertex_count == 0:
            print("<empty graph>")
        else:
            labels = [str(v.label) for v in self._vertices]
            max_label_len = max(map(len, labels))
            print(" " * (max_label_len + 3), end="")
            # Print labels formatted left-aligned in columns.
            print(" ".join(["{:<{}}".format(label, max_label_len) for label in labels]))
            for v1 in self._vertices:
                # Print label right-aligned in first column.
                print("{:>{}} : ".format(v1.label, max_label_len), end="")
                row = [int(v1.is_adjacent(v2)) for v2 in self._vertices]
                # Format cells left-aligned in columns.
                row = map(lambda cell: "{:<{}}".format(cell, max_label_len), row)
                print(" ".join(row))

    def depth_first(self) -> Iterator[DSAGraphVertex]:
        self._mark_nonvisited()
        stack = DSAStack()
        v: DSAGraphVertex = self._vertices.peek_first()
        yield v
        v.visited = True
        stack.push(v)
        while not stack.is_empty():
            for w in v.adjacent:
                if not w.visited:
                    yield w
                    w.visited = True
                    stack.push(w)
            v = stack.pop()

    def breadth_first(self) -> Iterator[DSAGraphVertex]:
        self._mark_nonvisited()
        queue = DSAQueue()
        v: DSAGraphVertex = self._vertices.peek_first()
        yield v
        v.visited = True
        queue.enqueue(v)
        while not queue.is_empty():
            v = queue.dequeue()
            for w in v.adjacent:
                if not w.visited:
                    yield w
                    w.visited = True
                    queue.enqueue(w)

    def _mark_nonvisited(self) -> None:
        for v in self._vertices:
            v.visited = False
