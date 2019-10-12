from dsa import Set, SinglyLinkedList

from itertools import chain
from typing import Iterator


__all__ = [
    "Person",
    "Post",
    "SocialNetwork"
]


class Person:
    def __init__(self, name: str, network: "SocialNetwork") -> None:
        self._name = name
        self._network = network
        self._posts = SinglyLinkedList()
        self._followers = Set(network._expected_people)
        self._following = Set(network._expected_people)
        self._liked_posts = Set(network._expected_posts)

    @property
    def name(self) -> str:
        return self._name

    # Posts are ordered most recent first.
    @property
    def posts(self) -> Iterator["Post"]:
        return iter(self._posts)

    @property
    def followers(self) -> Iterator["Person"]:
        return iter(self._followers)

    @property
    def following(self) -> Iterator["Person"]:
        return iter(self._following)

    @property
    def liked_posts(self) -> Iterator["Post"]:
        return iter(self._liked_posts)

    @property
    def post_count(self) -> int:
        return len(self._posts)

    @property
    def follower_count(self) -> int:
        return len(self._followers)

    @property
    def following_count(self) -> int:
        return len(self._following)

    @property
    def liked_post_count(self) -> int:
        return len(self._liked_posts)

    def make_post(self, text: str) -> "Post":
        post = Post(self, text)
        self._posts.insert_first(post)
        return post

    def follow(self, person: "Person") -> None:
        if person is self:
            raise ValueError(f"Cannot follow self.")
        if not self._following.add(person):
            raise ValueError(f"{person} already follows {self}.")
        person._followers.add(self)

    def like_post(self, post: "Post") -> None:
        if not self._liked_posts.add(post):
            raise ValueError(f"{self} already likes {post}.")
        post._like(self)

    def is_following(self, person: "Person") -> bool:
        return person in self._following

    def is_followed_by(self, person: "Person") -> bool:
        return person in self._followers

    def likes_post(self, post: "Post") -> bool:
        return post in self._liked_posts

    def __hash__(self) -> int:
        # People are actually unique, so can just use object identity.
        return id(self)

    def __repr__(self) -> str:
        return f"Person(name={self._name})"


class Post:
    def __init__(self, poster: Person, text: str) -> None:
        self._poster = poster
        self._text = text
        self._liked_by = Set(self._poster._network._expected_people)

    @property
    def poster(self) -> Person:
        return self._poster

    @property
    def text(self) -> str:
        return self._text

    @property
    def likers(self) -> Iterator[Person]:
        return iter(self._liked_by)

    @property
    def like_count(self) -> int:
        return len(self._liked_by)

    def is_liked_by(self, person: Person) -> bool:
        return person in self._liked_by

    def __hash__(self) -> int:
        # Posts are actually unique, so can just use object identity.
        return id(self)

    def __repr__(self) -> str:
        return f"Post(poster={self._poster}, text={self._text})"

    def _like(self, person: Person) -> None:
        self._liked_by.add(person)


class SocialNetwork:
    # expected_people: expected total number of people to be present in the network.
    # expected_post: expected total number of posts to be present in the network.
    # (These are solely for performance optimisation.)
    def __init__(self, expected_people: int, expected_posts: int) -> None:
        self._people = SinglyLinkedList()
        self._expected_people = max(expected_people, 1)
        self._expected_posts = max(expected_posts, 1)

    @property
    def person_count(self) -> int:
        return len(self._people)

    @property
    def people(self) -> Iterator[Person]:
        return iter(self._people)

    @property
    def posts(self) -> Iterator[Post]:
        return chain.from_iterable(person.posts for person in self.people)

    def add_person(self, name) -> Person:
        person = Person(name, self)
        self._people.insert_last(person)
        return person
