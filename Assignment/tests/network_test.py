from dsa import SinglyLinkedList
from network import SocialNetwork

import pickle
from unittest import TestCase


__all__ = [
    "SocialNetworkTest"
]


class SocialNetworkTest(TestCase):
    TEST_SIZE = 200

    def setUp(self) -> None:
        self._network = SocialNetwork()

    def test_add_person(self) -> None:
        people = SinglyLinkedList()
        for i in range(self.TEST_SIZE):
            name = str(i)
            person = self._network.add_person(name)
            people.insert_last(person)
            self.assertEqual(person, self._network.find_person(name))
            self.assertEqual(i + 1, self._network.person_count)
            for p in self._network.people:
                self.assertIn(p, people)

            self.assertEqual(name, person.name)
            self.assertEqual(0, person.following_count)
            self.assertEqual(0, person.follower_count)
            self.assertEqual(0, person.liked_post_count)
            self.assertEqual(0, person.post_count)
            for _ in person.following:
                self.fail()
            for _ in person.followers:
                self.fail()
            for _ in person.liked_posts:
                self.fail()
            for _ in person.posts:
                self.fail()

        for person in people:
            with self.assertRaises(ValueError):
                self._network.add_person(person.name)

    def test_delete_person_1(self) -> None:
        people = SinglyLinkedList()
        for i in range(self.TEST_SIZE):
            person = self._network.add_person(str(i))
            people.insert_last(person)

        for i, person in enumerate(people, 1):
            self._network.delete_person(person)
            self.assertEqual(len(people) - i, self._network.person_count)
            with self.assertRaises(ValueError):
                self._network.find_person(person.name)

        for _ in self._network.people:
            self.fail()

        for person in people:
            with self.assertRaises(ValueError):
                self._network.delete_person(person)

    def test_delete_person_2(self) -> None:
        person1 = self._network.add_person("Jeff")
        post = person1.make_post("Hello!")

        person2 = self._network.add_person("Lisa")
        person2.follow(person1)
        person2.like_post(post)

        self._network.delete_person(person2)
        self.assertNotIn(person2, person1.followers)
        self.assertEqual(0, person1.follower_count)
        self.assertNotIn(person2, post.liked_by)
        self.assertEqual(0, post.like_count)

    def test_make_post(self) -> None:
        person = self._network.add_person("Bill")
        post = person.make_post("Greetings.")
        self.assertEqual(1, person.post_count)
        self.assertEqual(1, self._network.post_count)
        for p in person.posts:
            self.assertEqual(post, p)
        self.assertEqual(person, post.poster)
        self.assertEqual("Greetings.", post.text)
        self.assertEqual(1, post.clickbait_factor)
        self.assertEqual(0, post.like_count)
        for _ in post.liked_by:
            self.fail()

    def test_follow(self) -> None:
        person1 = self._network.add_person("Carlos")
        person2 = self._network.add_person("Kenny")

        with self.assertRaises(ValueError):
            person1.follow(person1)
        self.assertFalse(person1.is_following(person1))
        self.assertFalse(person1.is_followed_by(person1))
        self.assertEqual(0, person1.following_count)
        self.assertEqual(0, person1.follower_count)

        person1.follow(person2)
        self.assertEqual(1, person1.following_count)
        self.assertEqual(1, person2.follower_count)
        self.assertTrue(person1.is_following(person2))
        self.assertIn(person2, person1.following)
        self.assertTrue(person2.is_followed_by(person1))
        self.assertIn(person1, person2.followers)
        self.assertFalse(person2.is_following(person1))
        self.assertNotIn(person1, person2.following)
        self.assertFalse(person1.is_followed_by(person2))
        self.assertNotIn(person2, person1.followers)

        with self.assertRaises(ValueError):
            person1.follow(person2)
        self.assertEqual(1, person1.following_count)
        self.assertEqual(1, person2.follower_count)

        person2.follow(person1)

    def test_like_post(self) -> None:
        person1 = self._network.add_person("Jim")
        person2 = self._network.add_person("Duncan")
        post = person1.make_post("a post")
        person2.like_post(post)
        self.assertEqual(1, person2.liked_post_count)
        self.assertEqual(1, post.like_count)
        self.assertIn(post, person2.liked_posts)
        self.assertTrue(person2.likes_post(post))

        with self.assertRaises(ValueError):
            person2.like_post(post)
        self.assertEqual(1, person2.liked_post_count)
        self.assertEqual(1, post.like_count)

    def test_unfollow(self) -> None:
        person1 = self._network.add_person("Bob")
        person2 = self._network.add_person("Grant")
        with self.assertRaises(ValueError):
            person1.unfollow(person2)
        with self.assertRaises(ValueError):
            person1.unfollow(person1)
        person1.follow(person2)
        person1.unfollow(person2)
        self.assertFalse(person1.is_following(person2))
        self.assertFalse(person2.is_followed_by(person1))
        self.assertEqual(0, person1.following_count)
        self.assertEqual(0, person2.follower_count)
        self.assertNotIn(person1, person2.followers)
        self.assertNotIn(person2, person1.following)

    def test_serialise_1(self) -> None:
        person1 = self._network.add_person("Rhys")
        person2 = self._network.add_person("Tracey")
        person3 = self._network.add_person("Aaron")
        person2.like_post(person1.make_post("Hello there"))
        person1.follow(person2)
        person3.follow(person2)
        network: SocialNetwork = pickle.loads(pickle.dumps(self._network))
        person1 = network.find_person("Rhys")
        person2 = network.find_person("Tracey")
        person3 = network.find_person("Aaron")
        self.assertEqual(3, network.person_count)
        self.assertEqual(1, network.post_count)
        self.assertTrue(person1.is_following(person2))
        self.assertTrue(person3.is_following(person2))

    def test_serialise_2(self) -> None:
        # Previously had trouble with hashing across serialisation.

        for i in range(self.TEST_SIZE):
            self._network.add_person(str(i))
        network: SocialNetwork = pickle.loads(pickle.dumps(self._network))
        for i in range(self.TEST_SIZE):
            network.find_person(str(i))
        for i in range(self.TEST_SIZE):
            with self.assertRaises(ValueError):
                network.add_person(str(i))
