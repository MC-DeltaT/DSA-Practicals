from dsa_heap import DSAHeap, _trickle_down, _trickle_up, heapify, heapsort

import unittest


class DSAHeapTest(unittest.TestCase):
    TEST_SIZE = 1000

    def setUp(self) -> None:
        ...

    def test_trickle_down1(self) -> None:
        # Root node belongs in bottom level.

        # Bottom level of tree full.
        array = [0, 10, 9, 7, 8, 6, 5]
        _trickle_down(array)
        expected = [10, 8, 9, 7, 0, 6, 5]
        self.assertListEqual(expected, array)

        # Bottom level of tree not full.
        array = [0, 9, 10, 7, 8, 6, 5, 4]
        _trickle_down(array)
        expected = [10, 9, 6, 7, 8, 0, 5, 4]
        self.assertListEqual(expected, array)

    def test_trickle_down2(self) -> None:
        # Root node belongs above bottom level.

        # Bottom level of tree full.
        array = [8, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 4]
        _trickle_down(array)
        expected = [12, 10, 11, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 4]
        self.assertListEqual(expected, array)

        # Bottom level of tree not full.
        array = [8, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 4, 2]
        _trickle_down(array)
        expected = [12, 10, 11, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 4, 2]
        self.assertListEqual(expected, array)

        # Root node belongs at root.
        array = [8, 6, 7, 5, 4, 2, 1, 0]
        _trickle_down(array)
        expected = [8, 6, 7, 5, 4, 2, 1, 0]
        self.assertListEqual(expected, array)

    def test_trickle_up1(self) -> None:
        # Last node belongs at root.

        # Bottom level of tree full.
        array = [9, 8, 7, 5, 6, 4, 3, 10]
        _trickle_up(array)
        expected = [10, 9, 7, 8, 6, 4, 3, 5]
        self.assertListEqual(expected, array)

        # Bottom level of tree not full.
        array = [9, 8, 7, 5, 6, 4, 10]
        _trickle_up(array)
        expected = [10, 8, 9, 5, 6, 4, 7]
        self.assertListEqual(expected, array)

    def test_trickle_up2(self) -> None:
        # Last node doesn't belong at root.

        # Bottom level of tree full.
        array = [14, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 13]
        _trickle_up(array)
        expected = [14, 12, 13, 10, 9, 8, 11, 6, 5, 4, 3, 2, 1, 0, 7]
        self.assertListEqual(expected, array)

        # Bottom level of tree not full.
        array = [14, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 5, 11]
        _trickle_up(array)
        expected = [14, 12, 11, 11, 9, 8, 7, 10, 5, 4, 3, 2, 1, 0, 5, 6]
        self.assertListEqual(expected, array)


if __name__ == "__main__":
    unittest.main()
