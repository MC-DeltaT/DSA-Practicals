from dsa_shuffling_queue import DSAShufflingQueue
from dsa_circular_queue import DSACircularQueue

from unittest import TestCase


# Inherit from this class and TestCase, and set attribute queue_cls to the
# desired DSAQueue conrete class to test.
class DSAQueueTest:
    max_queue_size = 10

    def setUp(self) -> None:
        self._queue = self.queue_cls(self.max_queue_size)

    def test_enqueue(self) -> None:
        for i in range(self.max_queue_size):
            self._queue.enqueue(i)
            self.assertEqual(0, self._queue.peek())
        with self.assertRaises(ValueError):
            self._queue.enqueue(42)

    def test_dequeue(self) -> None:
        with self.assertRaises(ValueError):
            self._queue.dequeue()
        for i in range(self.max_queue_size):
            self._queue.enqueue(i)
        for i in range(self.max_queue_size):
            self.assertEqual(i, self._queue.dequeue())
        with self.assertRaises(ValueError):
            self._queue.dequeue()

    def test_is_empty(self) -> None:
        self.assertTrue(self._queue.is_empty())
        for i in range(self.max_queue_size):
            self._queue.enqueue(i)
            self.assertFalse(self._queue.is_empty())
        for i in range(self.max_queue_size):
            self.assertFalse(self._queue.is_empty())
            self._queue.dequeue()
        self.assertTrue(self._queue.is_empty())
        
    def test_is_full(self) -> None:
        for i in range(self.max_queue_size):
            self.assertFalse(self._queue.is_full())
            self._queue.enqueue(i)
        self.assertTrue(self._queue.is_full())
        for i in range(self.max_queue_size):
            self._queue.dequeue()
            self.assertFalse(self._queue.is_full())

    def test_get_size(self) -> None:
        self.assertEqual(0, self._queue.get_size())
        for i in range(self.max_queue_size):
            self._queue.enqueue(i)
            self.assertEqual(i + 1, self._queue.get_size())
        for i in range(self.max_queue_size - 1, -1, -1):
            self._queue.dequeue()
            self.assertEqual(i, self._queue.get_size())


class DSAShufflingQueueTest(DSAQueueTest, TestCase):
    queue_cls = DSAShufflingQueue


class DSACircularQueueTest(DSAQueueTest, TestCase):
    queue_cls = DSACircularQueue
