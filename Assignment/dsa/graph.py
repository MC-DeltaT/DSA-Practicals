# Sourced from my Data Structures & Algorithms practical worksheet 5 submission,
# with modifications.

from . import LinkedList

from typing import Any, Iterator, Optional


__all__ = [
    "Graph",
    "GraphVertex",
    "GraphEdge"
]


class GraphVertex:
    def __init__(self, label: Any, value: Optional[Any] = None) -> None:
        self._label = label
        self._value = value
        self._edges = LinkedList()
        self.visited: bool = False

    @property
    def label(self) -> Any:
        return self._label

    @property
    def value(self) -> Any:
        return self._value

    @property
    def out_edges(self) -> Iterator:
        return iter(self._edges)

    @property
    def adjacent(self) -> Iterator:
        return (edge.sink for edge in self._edges)

    @property
    def outdegree(self) -> int:
        return len(self._edges)

    def is_adjacent(self, vertex) -> bool:
        return vertex in self.adjacent

    def has_adjacent(self, label: Any) -> bool:
        return label in map(lambda v: v.label, self.adjacent)

    def __str__(self) -> str:
        res = str(self.label)
        if self.value is not None:
            res = res + " value={}".format(self.value)
        return res

    def __repr__(self) -> str:
        return "GraphVertex(label={}, value={})".format(self.label, self.value)

    def __eq__(self, other) -> bool:
        return isinstance(other, GraphVertex) and other.label == self.label

    def _add_edge(self, edge) -> None:
        if self.is_adjacent(edge.sink):
            raise ValueError(
                "Vertex labelled `{}` already has an adjacent vertex labelled `{}`."
                    .format(self.label, edge.sink.label))
        self._edges.insert_last(edge)


class GraphEdge:
    def __init__(self, source: GraphVertex, sink: GraphVertex,
                 label: Optional[Any] = None, value: Optional[Any] = None) -> None:
        self._label = label
        self._value = value
        self._source = source
        self._sink = sink

    @property
    def label(self) -> Any:
        return self._label

    @property
    def value(self) -> Any:
        return self._value

    @property
    def source(self) -> GraphVertex:
        return self._source

    @property
    def sink(self) -> GraphVertex:
        return self._sink


class Graph:
    def __init__(self) -> None:
        self._vertices: LinkedList = LinkedList()

    @property
    def vertices(self) -> Iterator[GraphVertex]:
        return iter(self._vertices)

    @property
    def labels(self) -> Iterator[Any]:
        return map(lambda v: v.label, self._vertices)

    @property
    def is_empty(self) -> bool:
        return self._vertices.is_empty

    @property
    def vertex_count(self) -> int:
        return len(self._vertices)

    @property
    def edge_count(self) -> int:
        return sum(v.outdegree for v in self._vertices)

    def add_vertex(self, label: Any, value: Optional[Any] = None) -> None:
        if self.has_vertex(label):
            raise ValueError(f"Vertex labelled `{label}` already exists in graph.")
        self._vertices.insert_last(GraphVertex(label, value))

    def has_vertex(self, label: Any) -> bool:
        return label in map(lambda v: v.label, self._vertices)

    def get_vertex(self, label: Any) -> GraphVertex:
        try:
            return next(filter(lambda v: v.label == label, self._vertices))
        except StopIteration:
            raise ValueError(f"Vertex labelled `{label}` does not exist in graph.")

    def add_edge(self, source_label: Any, sink_label: Any,
                 edge_label: Optional[Any] = None, edge_value: Optional[Any] = None) -> None:
        source = self.get_vertex(source_label)
        sink = self.get_vertex(sink_label)
        edge = GraphEdge(source, sink, edge_label, edge_value)
        source._add_edge(edge)

    def get_adjacent(self, label: Any) -> Iterator[GraphVertex]:
        return self.get_vertex(label).adjacent

    def get_out_edges(self, label: Any) -> Iterator[GraphEdge]:
        return self.get_vertex(label).out_edges

    def is_adjacent(self, source_label: Any, sink_label: Any) -> bool:
        source = self.get_vertex(source_label)
        return source.has_adjacent(sink_label)

    def display_as_list(self) -> None:
        if self.vertex_count == 0:
            print("<empty graph>")
        else:
            for v1 in self._vertices:
                print("{} : ".format(v1.label), end="")
                print(", ".join(map(lambda v: str(v.label), v1.adjacent)))

    def display_as_matrix(self) -> None:
        if self.is_empty:
            print("<empty graph>")
        else:
            labels = [str(v.label) for v in self._vertices]
            max_label_len = max(map(len, labels))
            print(" " * (max_label_len + 3), end="")
            # Print labels formatted left-aligned in columns.
            print(" ".join("{:<{}}".format(label, max_label_len) for label in labels))
            for v1 in self._vertices:
                # Print label right-aligned in first column.
                print("{:>{}} : ".format(v1.label, max_label_len), end="")
                row = (int(v1.is_adjacent(v2)) for v2 in self._vertices)
                # Format cells left-aligned in columns.
                row = map(lambda cell: "{:<{}}".format(cell, max_label_len), row)
                print(" ".join(row))

    # def depth_first(self) -> Iterator[GraphVertex]:
    #     if not self.is_empty:
    #         self._mark_nonvisited()
    #         stack = DSAStack()
    #         cur: GraphVertex = min(self._vertices, key=lambda v: v.label)
    #         stack.push(cur)
    #         while not stack.is_empty():
    #             cur = stack.pop()
    #             if not cur.visited:
    #                 yield cur
    #                 cur.visited = True
    #                 for adjacent in sorted(cur.adjacent, key=lambda v: v.label, reverse=True):
    #                     stack.push(adjacent)
    #
    # def breadth_first(self) -> Iterator[GraphVertex]:
    #     if not self.is_empty:
    #         self._mark_nonvisited()
    #         queue = DSAQueue()
    #         cur: GraphVertex = min(self._vertices, key=lambda v: v.label)
    #         yield cur
    #         cur.visited = True
    #         queue.enqueue(cur)
    #         while not queue.is_empty():
    #             cur = queue.dequeue()
    #             for adjacent in sorted(cur.adjacent, key=lambda v: v.label):
    #                 if not adjacent.visited:
    #                     yield adjacent
    #                     adjacent.visited = True
    #                     queue.enqueue(adjacent)
    #
    # def _mark_nonvisited(self) -> None:
    #     for v in self._vertices:
    #         v.visited = False
