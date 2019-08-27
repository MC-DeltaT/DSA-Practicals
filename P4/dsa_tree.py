from math import floor, log2
from operator import lt
from typing import Any, Callable, Generator, Iterator, List, Tuple


class DSABinarySearchTree:
    class Node:
        def __init__(self, key: Any, value: Any, left=None, right=None) -> None:
            self.key = key
            self.value = value
            self.left = left
            self.right = right

        def __str__(self) -> str:
            return "k={}, v={}".format(self.key, self.value)

    def __init__(self, comparator: Callable[[Any, Any], bool] = lt) -> None:
        self._root = None
        self._comp = comparator

    @property
    def comparator(self) -> Callable[[Any, Any], bool]:
        return self._comp

    def find(self, key: Any) -> Any:
        def _find(node) -> Any:
            if node is None:
                raise ValueError("Key `{}` not found.".format(key))
            elif self._comp(key, node.key):
                value = _find(node.left)
            elif self._comp(node.key, key):
                value = _find(node.right)
            else:
                value = node.value
            return value

        return _find(self._root)

    def insert(self, key: Any, value: Any) -> None:
        def _insert(node):
            if node is None:
                update_node = self.Node(key, value)
            elif self._comp(key, node.key):
                node.left = _insert(node.left)
                update_node = node
            elif self._comp(node.key, key):
                node.right = _insert(node.right)
                update_node = node
            else:
                raise ValueError("Key `{}` already exists.".format(key))
            return update_node

        if self.is_empty():
            self._root = self.Node(key, value)
        else:
            _insert(self._root)

    def delete(self, key) -> None:
        def _promote_successor(node):
            if node.left is None:
                succ = node
            else:
                succ = _promote_successor(node.left)
                if succ is node.left:
                    node.left = succ.right

            return succ

        def _delete_node(node):
            if node.left is None and node.right is None:
                update_node = None
            elif node.left is not None and node.right is None:
                update_node = node.left
            elif node.left is None and node.right is not None:
                update_node = node.right
            else:
                update_node = _promote_successor(node.right)
                if update_node is not node.right:
                    update_node.right = node.right
                update_node.left = node.left
            return update_node

        def _delete(node):
            if node is None:
                raise ValueError("Key `{}` is not in tree.".format(key))
            elif self._comp(key, node.key):
                node.left = _delete(node.left)
                update_node = node
            elif self._comp(node.key, key):
                node.right = _delete(node.right)
                update_node = node
            else:
                update_node = _delete_node(node)
            return update_node

        self._root = _delete(self._root)

    def is_empty(self) -> bool:
        return self._root is None

    def min_key(self) -> Any:
        def _min_key(node) -> Any:
            if node.left:
                value = _min_key(node.left)
            else:
                value = node.key
            return value

        self._raise_if_empty()
        return _min_key(self._root)

    def max_key(self) -> Any:
        def _max_key(node) -> Any:
            if node.right:
                value = _max_key(node.right)
            else:
                value = node.key
            return value

        self._raise_if_empty()
        return _max_key(self._root)

    def height(self) -> int:
        def _height(node) -> int:
            if node:
                height = max(_height(node.left), _height(node.right)) + 1
            else:
                height = 0
            return height

        return _height(self._root)

    def balance(self) -> float:
        # Balance is evaluated by comparing how many nodes are missing from
        # each level compared to the perfectly balanced tree of the same size.
        # Gives a rough percentage of the nodes that can be found in log time.

        def _balance(node, depths: List[int], cur_depth: int) -> None:
            if node:
                depths.append(cur_depth)
                _balance(node.left, depths, cur_depth + 1)
                _balance(node.right, depths, cur_depth + 1)

        if self.is_empty():
            res = 1.0
        else:
            depths = []
            _balance(self._root, depths, 1)
            depths.sort()
            size = len(depths)
            ideal_height = floor(log2(size) + 1)
            nodes_per_level = [depths.count(i + 1) for i in range(ideal_height)]
            correct_nodes = sum(nodes_per_level)
            res = correct_nodes / size
        return res

    def in_order(self) -> Iterator[Tuple[Any, Any]]:
        def _in_order(node) -> Generator[Tuple[Any, Any], None, None]:
            if node:
                for t in _in_order(node.left):
                    yield t
                yield node.key, node.value
                for t in _in_order(node.right):
                    yield t

        return _in_order(self._root)

    def pre_order(self) -> Iterator[Tuple[Any, Any]]:
        def _pre_order(node) -> Generator[Tuple[Any, Any], None, None]:
            if node:
                yield node.key, node.value
                for t in _pre_order(node.left):
                    yield t
                for t in _pre_order(node.right):
                    yield t

        return _pre_order(self._root)

    def post_order(self) -> Iterator[Tuple[Any, Any]]:
        def _post_order(node) -> Generator[Tuple[Any, Any], None, None]:
            if node:
                for t in _post_order(node.left):
                    yield t
                for t in _post_order(node.right):
                    yield t
                yield node.key, node.value

        return _post_order(self._root)

    def display(self) -> None:
        def _display(node, level: int, prefix: str) -> None:
            if node:
                print("  " * level, end="")
                print(prefix + ": ", end="")
                print(node)
                _display(node.left, level + 1, "L")
                _display(node.right, level + 1, "R")

        if self.is_empty():
            print("<empty tree>")
        else:
            _display(self._root, 0, "Root")

    def __len__(self) -> int:
        return len(list(self.in_order()))

    def _raise_if_empty(self) -> None:
        if self.is_empty():
            raise ValueError("Tree is empty.")
