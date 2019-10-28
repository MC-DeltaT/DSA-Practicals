from dsa_queue import DSAQueue

import unittest


class DSAQueueTest(unittest.TestCase):
    test_size = 1000

    def setUp(self) -> None:
        self._queue = DSAQueue()

    def test_enqueue(self) -> None:
        for i in range(self.test_size):
            self._queue.enqueue(i)
            self.assertEqual(0, self._queue.peek())

    def test_dequeue(self) -> None:
        with self.assertRaises(ValueError):
            self._queue.dequeue()
        for i in range(self.test_size):
            self._queue.enqueue(i)
        for i in range(self.test_size):
            self.assertEqual(i, self._queue.dequeue())
        with self.assertRaises(ValueError):
            self._queue.dequeue()

    def test_is_empty(self) -> None:
        self.assertTrue(self._queue.is_empty())
        for i in range(self.test_size):
            self._queue.enqueue(i)
            self.assertFalse(self._queue.is_empty())
        for i in range(self.test_size):
            self.assertFalse(self._queue.is_empty())
            self._queue.dequeue()
        self.assertTrue(self._queue.is_empty())
    
    def test_iter(self) -> None:
        for e in self._queue:
            self.fail()

        for i in range(self.test_size):
            self._queue.enqueue(i)
            for j, e in enumerate(self._queue):
                self.assertEqual(j, e) 


if __name__ == "__main__":
    unittest.main(verbosity=2)
