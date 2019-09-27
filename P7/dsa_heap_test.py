from dsa_heap import DSAHeap, _trickle_down, _trickle_up, heapify, heapsort

from itertools import takewhile
import random
from typing import Sequence
import unittest


class DSAHeapToolsTest(unittest.TestCase):
    TEST_SIZE = 1000

    def test_trickle_down_1(self) -> None:
        # Root node belongs in bottom level.

        # Bottom level of tree full.
        array = [0, 10, 9, 7, 8, 6, 5]
        expected = [10, 8, 9, 7, 0, 6, 5]
        _trickle_down(array)
        self.assertListEqual(expected, array)

        # Bottom level of tree not full.
        array = [0, 9, 10, 7, 8, 6, 5, 4]
        expected = [10, 9, 6, 7, 8, 0, 5, 4]
        _trickle_down(array)
        self.assertListEqual(expected, array)

    def test_trickle_down_2(self) -> None:
        # Root node belongs above bottom level.

        # Bottom level of tree full.
        array = [8, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 4]
        expected = [12, 10, 11, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 4]
        _trickle_down(array)
        self.assertListEqual(expected, array)

        # Bottom level of tree not full.
        array = [8, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 4, 2]
        expected = [12, 10, 11, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 4, 2]
        _trickle_down(array)
        self.assertListEqual(expected, array)

        # Root node belongs at root.
        array = [8, 6, 7, 5, 4, 2, 1, 0]
        expected = [8, 6, 7, 5, 4, 2, 1, 0]
        _trickle_down(array)
        self.assertListEqual(expected, array)

    def test_trickle_down_3(self) -> None:
        # Edge cases.

        # 0 elements.
        array = []
        expected = []
        _trickle_down(array)
        self.assertListEqual(expected, array)

        # 1 element.
        array = [10]
        expected = [10]
        _trickle_down(array)
        self.assertListEqual(expected, array)

        # 2 elements.
        array = [5, 10]
        expected = [10, 5]
        _trickle_down(array)
        self.assertListEqual(expected, array)

    def test_trickle_up_1(self) -> None:
        # Last node belongs at root.

        # Bottom level of tree full.
        array = [9, 8, 7, 5, 6, 4, 3, 10]
        expected = [10, 9, 7, 8, 6, 4, 3, 5]
        _trickle_up(array)
        self.assertListEqual(expected, array)

        # Bottom level of tree not full.
        array = [9, 8, 7, 5, 6, 4, 10]
        expected = [10, 8, 9, 5, 6, 4, 7]
        _trickle_up(array)
        self.assertListEqual(expected, array)

    def test_trickle_up_2(self) -> None:
        # Last node doesn't belong at root.

        # Bottom level of tree full.
        array = [14, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 13]
        expected = [14, 12, 13, 10, 9, 8, 11, 6, 5, 4, 3, 2, 1, 0, 7]
        _trickle_up(array)
        self.assertListEqual(expected, array)

        # Bottom level of tree not full.
        array = [14, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 5, 11]
        expected = [14, 12, 11, 11, 9, 8, 7, 10, 5, 4, 3, 2, 1, 0, 5, 6]
        _trickle_up(array)
        self.assertListEqual(expected, array)

    def test_trickle_up_3(self) -> None:
        # Edge cases.

        # 0 elements.
        array = []
        expected = []
        _trickle_up(array)
        self.assertListEqual(expected, array)

        # 1 element.
        array = [10]
        expected = [10]
        _trickle_up(array)
        self.assertListEqual(expected, array)

        # 2 elements.
        array = [3, 7]
        expected = [7, 3]
        _trickle_up(array)
        self.assertListEqual(expected, array)

    def test_heapify_1(self) -> None:
        # Array already forms a heap.

        # Bottom level of tree full.
        array = [15, 14, 14, 13, 10, 11, 9, 12, 12, 9, 4, 10, 8, 8, 2]
        expected = array.copy()
        heapify(array)
        self.assertListEqual(expected, array)

        # Bottom level of tree not full.
        array = [15, 14, 14, 13, 10, 11, 9, 12, 12, 9, 4, 10, 8, 8, 2, 3, 1, 1]
        expected = array.copy()
        heapify(array)
        self.assertListEqual(expected, array)

    def test_heapify_2(self) -> None:
        # Array doesn't already form a heap.

        # Bottom level of tree full.
        array = [10, 7, 10, 14, 7, 8, 9]
        expected = [14, 10, 10, 7, 7, 8, 9]
        heapify(array)
        self.assertListEqual(expected, array)

        # Bottom level of tree not full.
        array = [6, 4, 8, 2, 10, 7, 0, 11]
        expected = [11, 10, 8, 4, 6, 7, 0, 2]
        heapify(array)
        self.assertListEqual(expected, array)

    def test_heapify_3(self) -> None:
        # Edge cases.

        # 0 elements.
        array = []
        expected = []
        heapify(array)
        self.assertListEqual(expected, array)

        # 1 element.
        array = [10]
        expected = [10]
        heapify(array)
        self.assertListEqual(expected, array)

        # 2 elements.
        array = [5, 10]
        expected = [10, 5]
        heapify(array)
        self.assertListEqual(expected, array)

    def test_heapify_4(self) -> None:
        # Automated random test cases.
        for n in range(self.TEST_SIZE):
            array = random.choices(range(self.TEST_SIZE), k=n)
            heapify(array)
            self.assertTrue(self._is_heap(array))

    def test_heapsort_1(self) -> None:
        # Automated random test cases.
        for n in range(self.TEST_SIZE):
            array = random.choices(range(self.TEST_SIZE), k=n)
            heapsort(array)
            self.assertListEqual(sorted(array), array)

    def test_heapsort_2(self) -> None:
        # Edge cases.

        # 0 elements.
        array = []
        expected = []
        heapsort(array)
        self.assertListEqual(expected, array)

        # 1 element.
        array = [5]
        expected = [5]
        heapsort(array)
        self.assertListEqual(expected, array)

    def test_heapsort_3(self) -> None:
        # Random but already sorted data.
        for n in range(self.TEST_SIZE):
            array = random.choices(range(self.TEST_SIZE), k=n)
            array = sorted(array)
            expected = array.copy()
            heapsort(array)
            self.assertListEqual(expected, array)

    @staticmethod
    def _is_heap(seq: Sequence) -> bool:
        res = True
        for i in takewhile(lambda _: res, range(1, len(seq))):
            res = seq[(i - 1) // 2] >= seq[i]
        return res


class DSAHeapTest(unittest.TestCase):
    TEST_SIZE = 10

    def setUp(self) -> None:
        self._heap = DSAHeap(self.TEST_SIZE)

    def test_add_remove(self) -> None:
        priorities = random.choices(range(self.TEST_SIZE), k=self.TEST_SIZE)
        values = random.choices(range(self.TEST_SIZE), k=self.TEST_SIZE)
        for p, v in zip(priorities, values):
            self._heap.add(v, p)

        # TODO: handle case where multiple values have the same priority (ordering not guaranteed).
        priorities, values = zip(*sorted(zip(priorities, values), key=lambda t: t[0], reverse=True))
        for v in values:
            self.assertEqual(v, self._heap.remove())


if __name__ == "__main__":
    unittest.main()
