from dsa_graph import DSAGraph, DSAGraphVertex

import random
from typing import Any, Dict, Sequence, Set, Tuple
import unittest


def simultaneous_shuffle(*sequences: Sequence[Any]) -> Tuple[Sequence[Any]]:
    tmp = list(zip(*sequences))
    random.shuffle(tmp)
    return (*zip(*tmp),)


class DSAGraphVertexTest(unittest.TestCase):
    TEST_SIZE = 1000

    def setUp(self) -> None:
        self._vertex = DSAGraphVertex("foo", "bar")

    def test_adjacent(self) -> None:
        # Add adjacent vertices.
        adjacent = [DSAGraphVertex(i) for i in range(self.TEST_SIZE)]
        random.shuffle(adjacent)
        for v in adjacent:
            self._vertex.add_adjacent(v)

        # Assert has added adjacent vertices.
        random.shuffle(adjacent)
        for v in adjacent:
            self.assertTrue(self._vertex.is_adjacent(v))

        # Assert set of adjacent vertices is correct.
        random.shuffle(adjacent)
        self.assertSetEqual(frozenset(adjacent), frozenset(self._vertex.adjacent))

        # Assert other arbitrary vertices are not adjacent.
        random.shuffle(adjacent)
        for v in (DSAGraphVertex(self.TEST_SIZE + i) for i in range(self.TEST_SIZE)):
            self.assertFalse(self._vertex.is_adjacent(v))

        # Assert can't re-add adjacent vertices.
        random.shuffle(adjacent)
        for v in adjacent:
            with self.assertRaises(ValueError):
                self._vertex.add_adjacent(v)


class DSAGraphTest(unittest.TestCase):
    TEST_SIZE = 75

    def setUp(self) -> None:
        self._graph = DSAGraph()
        random.seed()

    def test_vertices(self) -> None:
        # Add vertices.
        labels = list(range(self.TEST_SIZE))
        values = list(range(self.TEST_SIZE))
        simultaneous_shuffle(labels, values)
        for l, v in zip(labels, values):
            self._graph.add_vertex(l, v)

        # Assert has vertices just added.
        simultaneous_shuffle(labels, values)
        for l in labels:
            self.assertTrue(self._graph.has_vertex(l))

        # Assert vertex objects are correct.
        simultaneous_shuffle(labels, values)
        for l, v in zip(labels, values):
            vertex = self._graph.get_vertex(l)
            self.assertEqual(l, vertex.label)
            self.assertEqual(v, vertex.value)
            self.assertTrue(len(vertex.adjacent) == 0)

    def test_edges(self) -> None:
        # Add vertices
        labels = list(range(self.TEST_SIZE))
        for l in labels:
            self._graph.add_vertex(l)

        # Generate edges.
        edge_list: Set[Tuple[int, int]] = set()
        for l1 in labels:
            count = random.choice(range(len(labels)))
            for l2 in random.choices(labels, k=count):
                if l1 != l2:
                    edge_list.add((l1, l2))
        adjacency_list: Dict[int, Set[int]] = {l: set() for l in labels}
        for l1, l2 in edge_list:
            adjacency_list[l1].add(l2)
        nonadjacency_list = {l: set(labels) - adj for l, adj in adjacency_list.items()}

        # Add edges.
        for l1, l2 in edge_list:
            self._graph.add_edge(l1, l2)

        # Assert edges make vertices adjacent.
        for l1, l2 in edge_list:
            self.assertTrue(self._graph.is_adjacent(l1, l2))

        # Assert other vertices are not adjacent.
        for l1, nonadj in nonadjacency_list.items():
            for l2 in nonadj:
                self.assertFalse(self._graph.is_adjacent(l1, l2))

        # Assert set of adjacent vertices is correct.
        random.shuffle(labels)
        for l in labels:
            adj = frozenset(map(lambda v: v.label, self._graph.get_adjacent(l)))
            self.assertSetEqual(adjacency_list[l], adj)

        # Assert can't re-add edges.
        tmp = list(edge_list)
        random.shuffle(tmp)
        for l1, l2 in tmp:
            with self.assertRaises(ValueError):
                self._graph.add_edge(l1, l2)

    def test_vertex_count(self) -> None:
        labels = list(range(self.TEST_SIZE))

        # Assert vertex count follows addition of vertices.
        self.assertEqual(0, self._graph.vertex_count)
        for n, l in enumerate(labels, 1):
            self._graph.add_vertex(l)
            self.assertEqual(n, self._graph.vertex_count)

        # Assert adding edges doesn't screw up vertex count.
        edge_set = set()
        for l1 in labels:
            count = random.choice(range(len(labels)))
            for l2 in random.choices(labels, k=count):
                if l1 != l2:
                    edge_set.add((l1, l2))
        for l1, l2 in edge_set:
            self._graph.add_edge(l1, l2)
            self.assertEqual(len(labels), self._graph.vertex_count)

    def test_edge_count(self) -> None:
        # Assert empty graph has no edges.
        self.assertEqual(0, self._graph.edge_count)

        # Add vertices.
        labels = list(range(self.TEST_SIZE))
        for l in labels:
            self._graph.add_vertex(l)
            # Assert adding vertices doesn't screw up edge count.
            self.assertEqual(0, self._graph.edge_count)

        # Assert edge count follows addition of edges.
        edge_set = set()
        for l1 in labels:
            count = random.choice(range(len(labels)))
            for l2 in random.choices(labels, k=count):
                if l1 != l2:
                    edge_set.add((l1, l2))
        for n, (l1, l2) in enumerate(edge_set, 1):
            self._graph.add_edge(l1, l2)
            self.assertEqual(n, self._graph.edge_count)

    def test_is_empty(self) -> None:
        # Assert empty graph is empty.
        self.assertTrue(self._graph.is_empty)

        # Assert adding vertices makes graph non-empty.
        labels = list(range(min(15, self.TEST_SIZE)))
        for l in labels:
            self._graph.add_vertex(l)
            self.assertFalse(self._graph.is_empty)

        # Assert adding edges keeps graph non-empty.
        edge_set = set()
        for l1 in labels:
            count = random.choice(range(len(labels)))
            for l2 in random.choices(labels, k=count):
                if l1 != l2:
                    edge_set.add((l1, l2))
        for l1, l2 in edge_set:
            self._graph.add_edge(l1, l2)
            self.assertFalse(self._graph.is_empty)

    def test_breadth_first1(self) -> None:
        # Assert empty graph traverses nothing.
        for _ in self._graph.breadth_first():
            self.fail()

        # Add vertices.
        for label in "BGEFDAC":
            self._graph.add_vertex(label)

        # Add edges.
        for l1, l2 in ["FD", "FG", "FE",
                       "AB", "AD", "AC", "AE",
                       "BA", "BE",
                       "EB", "EG", "EF", "EA",
                       "DA", "DC", "DF",
                       "GF", "GE",
                       "CD", "CA"]:
            self._graph.add_edge(l1, l2)

        # Assert traversal is correct order and enumerates all vertices.
        breadth_first = [v.label for v in self._graph.breadth_first()]
        expected = list("ABCDEFG")
        self.assertListEqual(expected, breadth_first)

    def test_breadth_first2(self) -> None:
        # Add vertices.
        for label in "AIFDCBGHJE":
            self._graph.add_vertex(label)

        # Add edges.
        for l1, l2 in ["CA", "CF",
                       "IH", "IF", "IJ",
                       "AB", "AD", "AC",
                       "BA", "BE",
                       "EG", "ED", "EB",
                       "DF", "DH", "DA", "DE",
                       "FC", "FI", "FD",
                       "HI", "HD", "HJ", "HG",
                       "JI", "JH", "JG",
                       "GE", "GH", "GJ"]:
            self._graph.add_edge(l1, l2)

        # Assert traversal is correct order and enumerates all vertices.
        breadth_first = [v.label for v in self._graph.breadth_first()]
        expected = list("ABCDEFHGIJ")
        self.assertListEqual(expected, breadth_first)

    def test_depth_first1(self) -> None:
        # Assert empty graph traverses nothing.
        for _ in self._graph.depth_first():
            self.fail()

        # Add vertices.
        for label in "BGEFDAC":
            self._graph.add_vertex(label)

        # Add edges.
        for l1, l2 in ["FD", "FG", "FE",
                       "AB", "AD", "AC", "AE",
                       "BA", "BE",
                       "EB", "EG", "EF", "EA",
                       "DA", "DC", "DF",
                       "GF", "GE",
                       "CD", "CA"]:
            self._graph.add_edge(l1, l2)

        # Assert traversal is correct order and enumerates all vertices.
        depth_first = [v.label for v in self._graph.depth_first()]
        expected = list("ABEFDCG")
        self.assertListEqual(expected, depth_first)

    def test_depth_first2(self) -> None:
        # Add vertices.
        for label in "AIFDCBGHJE":
            self._graph.add_vertex(label)

        # Add edges.
        for l1, l2 in ["CA", "CF",
                       "IH", "IF", "IJ",
                       "AB", "AD", "AC",
                       "BA", "BE",
                       "EG", "ED", "EB",
                       "DF", "DH", "DA", "DE",
                       "FC", "FI", "FD",
                       "HI", "HD", "HJ", "HG",
                       "JI", "JH", "JG",
                       "GE", "GH", "GJ"]:
            self._graph.add_edge(l1, l2)

        # Assert traversal is correct order and enumerates all vertices.
        depth_first = [v.label for v in self._graph.depth_first()]
        expected = list("ABEDFCIHGJ")
        self.assertListEqual(expected, depth_first)

    def test_display_as_list(self) -> None:
        self._graph.display_as_list()
        print()

        # Add vertices.
        labels = list(range(min(15, self.TEST_SIZE)))
        for l in labels:
            self._graph.add_vertex(l)
            self.assertEqual(0, self._graph.edge_count)

        # Add edges.
        edge_set = set()
        for l1 in labels:
            count = random.choice(range(len(labels)))
            for l2 in random.choices(labels, k=count):
                if l1 != l2:
                    edge_set.add((l1, l2))
        for l1, l2 in edge_set:
            self._graph.add_edge(l1, l2)

        self._graph.display_as_list()
        print()

    def test_display_as_matrix(self) -> None:
        self._graph.display_as_matrix()
        print()

        # Add vertices.
        labels = list(range(min(15, self.TEST_SIZE)))
        for l in labels:
            self._graph.add_vertex(l)
            self.assertEqual(0, self._graph.edge_count)

        # Add edges.
        edge_set = set()
        for l1 in labels:
            count = random.choice(range(len(labels)))
            for l2 in random.choices(labels, k=count):
                if l1 != l2:
                    edge_set.add((l1, l2))
        for l1, l2 in edge_set:
            self._graph.add_edge(l1, l2)

        self._graph.display_as_matrix()
        print()


if __name__ == "__main__":
    unittest.main()
