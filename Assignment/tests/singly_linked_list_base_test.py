from dsa.impl import SinglyLinkedListBase

from unittest import TestCase


__all__ = [
    "SinglyLinkedListBaseTest"
]


class SinglyLinkedListBaseTest(TestCase):
    TEST_SIZE = 400

    def setUp(self) -> None:
        self._list = SinglyLinkedListBase()

    def test_init(self) -> None:
        self.assertIsNotNone(self._list.before_head)                # before_head set up correctly
        self.assertIsNone(self._list.before_head.data)
        self.assertIsNone(self._list.before_head.next)
        self.assertIsNone(self._list.head)                          # no head
        self.assertIs(self._list.tail, self._list.before_head)      # tail is before_head
        self.assertEqual(0, self._list.size)                        # size is 0

    def test_insert_first_1(self) -> None:
        before_head = self._list.before_head

        # 0 -> 1 item.
        self._list.insert_first(0)
        self.assertIsNotNone(self._list.head)                           # head updated correctly
        self.assertEqual(0, self._list.head.data)
        self.assertIsNone(self._list.head.next)
        self.assertIs(self._list.before_head.next, self._list.head)     # before_head.next updated correctly
        self.assertIs(self._list.tail, self._list.head)                 # tail updated correctly
        self.assertIs(self._list.before_head, before_head)              # before_head ref not changed
        self.assertIsNone(self._list.before_head.data)                  # before_head.data not changed
        self.assertEqual(1, self._list.size)                            # size correct

        # 1 -> 2 items.
        prev_head = self._list.head
        prev_tail = self._list.tail
        self._list.insert_first(1)
        self.assertIs(prev_tail, self._list.tail)                       # tail not changed
        self.assertEqual(0, self._list.tail.data)
        self.assertIsNone(self._list.tail.next)
        self.assertEqual(1, self._list.head.data)                       # head updated correctly
        self.assertIs(self._list.head.next, prev_head)
        self.assertIs(self._list.head.next, self._list.tail)
        self.assertIs(self._list.before_head.next, self._list.head)     # before_head.next updated correctly
        self.assertIs(self._list.before_head, before_head)              # before_head ref not changed
        self.assertIsNone(self._list.before_head.data)                  # before_head.data not changed
        self.assertEqual(2, self._list.size)                            # size correct

        # 2 -> 3 items.
        prev_head = self._list.head
        prev_tail = self._list.tail
        self._list.insert_first(2)
        self.assertIs(prev_tail, self._list.tail)                       # tail not changed
        self.assertEqual(0, self._list.tail.data)
        self.assertIsNone(self._list.tail.next)
        self.assertEqual(2, self._list.head.data)                       # head updated correctly
        self.assertIs(self._list.head.next, prev_head)
        self.assertIs(self._list.before_head.next, self._list.head)     # before_head.next updated correctly
        self.assertIs(self._list.before_head, before_head)              # before_head ref not changed
        self.assertIsNone(self._list.before_head.data)
        self.assertIs(prev_head.next, self._list.tail)                  # middle node preserved
        self.assertEqual(1, prev_head.data)
        self.assertEqual(3, self._list.size)                            # size correct

    def test_insert_first_2(self) -> None:
        # Automated test cases.
        before_head = self._list.before_head
        self._list.insert_first(-1)
        for i in range(self.TEST_SIZE):
            prev_head = self._list.head
            prev_tail = self._list.tail
            self._list.insert_first(i)
            self.assertIs(self._list.before_head, before_head)          # before_head ref not changed
            self.assertIs(self._list.before_head.next, self._list.head) # before_head.next updated correctly
            self.assertIs(self._list.head.next, prev_head)              # head.next set correctly
            self.assertIs(self._list.tail, prev_tail)                   # tail not changed
            self.assertIsNone(self._list.tail.next)
            self.assertEqual(-1, self._list.tail.data)
            self.assertEqual(i + 2, self._list.size)                    # size correct

    def test_insert_last(self) -> None:
        before_head = self._list.before_head

        # 0 -> 1 item.
        self._list.insert_last(0)
        self.assertIsNotNone(self._list.head)                           # head updated correctly
        self.assertEqual(0, self._list.head.data)
        self.assertIsNone(self._list.head.next)
        self.assertIs(self._list.before_head.next, self._list.head)     # before_head.next updated correctly
        self.assertIs(self._list.tail, self._list.head)                 # tail updated correctly
        self.assertIs(self._list.before_head, before_head)              # before_head ref not changed
        self.assertIsNone(self._list.before_head.data)                  # before_head.data not changed
        self.assertEqual(1, self._list.size)                            # size correct

        # 1 -> 2 items.
        prev_head = self._list.head
        self._list.insert_last(1)
        self.assertEqual(1, self._list.tail.data)                       # tail updated correctly
        self.assertIsNone(self._list.tail.next)
        self.assertIs(prev_head, self._list.head)                       # head ref not changed
        self.assertEqual(0, self._list.head.data)                       # head.data not changed
        self.assertIs(self._list.head.next, self._list.tail)            # head.next updated correctly
        self.assertIs(self._list.before_head, before_head)              # before_head not changed
        self.assertIsNone(self._list.before_head.data)
        self.assertIs(self._list.before_head.next, self._list.head)
        self.assertEqual(2, self._list.size)                            # size correct

        # 2 -> 3 items.
        middle = self._list.tail
        prev_head = self._list.head
        self._list.insert_last(2)
        self.assertIs(prev_head, self._list.head)                       # head not changed
        self.assertEqual(0, self._list.head.data)
        self.assertIs(self._list.head.next, middle)
        self.assertIs(self._list.before_head, before_head)              # before_head not changed
        self.assertIsNone(self._list.before_head.data)
        self.assertIs(self._list.before_head.next, self._list.head)
        self.assertIs(middle.next, self._list.tail)                     # middle.next updated
        self.assertEqual(1, middle.data)                                # middle.data not changed
        self.assertEqual(2, self._list.tail.data)                       # tail updated correctly
        self.assertIsNone(self._list.tail.next)
        self.assertEqual(3, self._list.size)                            # size correct

    def test_find_1(self) -> None:
        # Automated test cases, inserting to front.
        for i in range(self.TEST_SIZE):
            self._list.insert_first(i)
            node = self._list.find(i)
            self.assertIs(node, self._list.head)
            self.assertEqual(i, node.data)

            for j in range(i):
                node = self._list.find(j)
                self.assertEqual(j, node.data)
                self.assertIsNot(node, self._list.head)

            for j in range(i + 1, self.TEST_SIZE):
                with self.assertRaises(ValueError):
                    self._list.find(j)

            self.assertEqual(i + 1, self._list.size)

    def test_find_2(self) -> None:
        # Automated test cases, inserting to back.
        for i in range(self.TEST_SIZE):
            self._list.insert_last(i)
            node = self._list.find(i)
            self.assertIs(node, self._list.tail)
            self.assertEqual(i, node.data)

            for j in range(i):
                node = self._list.find(j)
                self.assertEqual(j, node.data)
                self.assertIsNot(node, self._list.tail)

            for j in range(i + 1, self.TEST_SIZE):
                with self.assertRaises(ValueError):
                    self._list.find(j)

            self.assertEqual(i + 1, self._list.size)

    def test_find_3(self) -> None:
        # Empty list.
        for i in range(self.TEST_SIZE):
            with self.assertRaises(ValueError):
                self._list.find(i)
            self.assertEqual(0, self._list.size)

    def test_remove_after(self) -> None:
        before_head = self._list.before_head

        # 1 item, remove head.
        self._list.insert_first(0)
        self._list.remove_after(self._list.before_head)
        self.assertNotIn(0, self._list)                         # item removed
        self.assertIs(self._list.before_head, before_head)      # before_head not changed
        self.assertIsNone(self._list.before_head.next)
        self.assertIsNone(self._list.head)                      # no head
        self.assertIs(self._list.tail, self._list.before_head)  # tail set to before_head
        self.assertEqual(0, self._list.size)                    # size correct

        # 2 items, remove head.
        # List is currently empty.
        self._list.insert_last(0)
        self._list.insert_last(1)
        prev_tail = self._list.tail
        self._list.remove_after(self._list.before_head)
        self.assertNotIn(0, self._list)                             # item removed
        self.assertIs(self._list.before_head, before_head)          # before_head not changed
        self.assertIs(self._list.before_head.next, self._list.head)
        self.assertIs(self._list.tail, prev_tail)                   # tail not changed
        self.assertIsNone(self._list.tail.next)
        self.assertEqual(1, self._list.tail.data)
        self.assertIs(self._list.head, self._list.tail)             # head updated correctly
        self.assertIsNone(self._list.head.next)
        self.assertEqual(1, self._list.size)                        # size correct

        # 2 items, remove tail.
        # List is currently [1].
        self._list.insert_last(2)
        prev_head = self._list.head
        self._list.remove_after(self._list.head)
        self.assertNotIn(2, self._list)  # item removed
        self.assertIs(self._list.before_head, before_head)          # before_head not changed
        self.assertIs(self._list.before_head.next, self._list.head)
        self.assertIs(self._list.head, prev_head)                   # head ref not changed
        self.assertIsNone(self._list.head.next)                     # head.next set correctly
        self.assertEqual(1, self._list.head.data)                   # head.data preserved
        self.assertIs(self._list.tail, self._list.head)             # tail set correctly
        self.assertEqual(1, self._list.size)                        # size correct

    def test_remove(self) -> None:
        # Empty list.
        for i in range(self.TEST_SIZE):
            with self.assertRaises(ValueError):
                self._list.remove(i)

        before_head = self._list.before_head

        # 1 item, remove 1.
        self._list.insert_last(0)
        self._list.remove(0)
        self.assertNotIn(0, self._list)                         # item removed
        self.assertIs(self._list.before_head, before_head)      # before_head not changed
        self.assertIsNone(self._list.before_head.next)
        self.assertIsNone(self._list.head)                      # no head
        self.assertIs(self._list.tail, self._list.before_head)  # tail set to before_head
        self.assertEqual(0, self._list.size)                    # size is 0

        # 2 items, remove head.
        # List is currently empty.
        self._list.insert_last(0)
        self._list.insert_last(1)
        prev_tail = self._list.tail
        self._list.remove(0)
        self.assertNotIn(0, self._list)                                 # item removed
        self.assertIs(self._list.before_head, before_head)              # before_head not changed
        self.assertIs(self._list.before_head.next, self._list.head)
        self.assertIs(self._list.tail, prev_tail)                       # tail not changed
        self.assertIsNone(self._list.tail.next)
        self.assertEqual(1, self._list.tail.data)
        self.assertIs(self._list.head, self._list.tail)                 # head updated correctly
        self.assertIsNone(self._list.head.next)
        self.assertEqual(1, self._list.size)                            # size correct

        # 2 items, remove tail.
        # List is currently [1].
        self._list.insert_last(2)
        prev_head = self._list.head
        self._list.remove(2)
        self.assertNotIn(2, self._list)                                 # item removed
        self.assertIs(self._list.before_head, before_head)              # before_head not changed
        self.assertIs(self._list.before_head.next, self._list.head)
        self.assertIs(self._list.head, prev_head)                       # head ref not changed
        self.assertIsNone(self._list.head.next)                         # head.next set correctly
        self.assertEqual(1, self._list.head.data)                       # head.data preserved
        self.assertIs(self._list.tail, self._list.head)                 # tail set correctly
        self.assertEqual(1, self._list.size)                            # size correct

    def test_remove_all(self) -> None:
        before_head = self._list.before_head
        for i in range(self.TEST_SIZE):
            for j in range(i):
                self._list.insert_first(j)
            self._list.remove_all()
            self.assertIs(self._list.before_head, before_head)          # before_head not changed
            self.assertIsNone(self._list.before_head.next)
            self.assertIsNone(self._list.head)                          # no head
            self.assertIs(self._list.tail, self._list.before_head)      # tail set to before_head
            self.assertEqual(0, self._list.size)                        # size is 0

    def test_iter(self) -> None:
        for _ in self._list:
            self.fail("iter empty list")

        for i in range(self.TEST_SIZE):
            self._list.insert_first(i)
            for expected, actual in zip(reversed(range(i + 1)), self._list):
                self.assertEqual(expected, actual, "insert_first + iter")
        self._list.remove_all()
        for i in range(self.TEST_SIZE):
            self._list.insert_last(i)
            for expected, actual in zip(range(i + 1), self._list):
                self.assertEqual(expected, actual, "insert_last + iter")
