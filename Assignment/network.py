from common import hash_str
from dsa import OrderedSet, Set, SinglyLinkedList

from itertools import chain
from typing import Iterator


__all__ = [
    "Person",
    "Post",
    "SocialNetwork"
]


class Person:
    def __init__(self, name: str) -> None:
        self._name = name
        self._posts = SinglyLinkedList()
        self._followers = Set()
        self._following = Set()
        self._liked_posts = OrderedSet(100)
        self._next_post_id = 1

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
    def post_like_count(self) -> int:
        return len(self._liked_posts)

    def make_post(self, text: str) -> "Post":
        id = self._generate_post_id()
        post = Post(self, id, text)
        self._posts.insert_first(post)
        return post

    def follow(self, person: "Person") -> None:
        if person is self:
            raise ValueError(f"Cannot follow self.")
        if not self._following.add(person):
            raise ValueError(f"{person} already follows {self}.")
        person._followers.add(self)

    def like_post(self, post: "Post") -> None:
        if not self._liked_posts.add_first(post):
            raise ValueError(f"{self} already likes {post}.")
        post._like(self)

    def is_following(self, person: "Person") -> bool:
        return person in self._following

    def is_followed_by(self, person: "Person") -> bool:
        return person in self._followers

    def likes_post(self, post: "Post") -> bool:
        return post in self._liked_posts

    def __eq__(self, other) -> bool:
        return isinstance(other, Person) and other._name == self._name

    def __hash__(self) -> int:
        return hash_str(self._name)

    def __repr__(self) -> str:
        return f"Person(name={self._name})"

    def _generate_post_id(self) -> int:
        id = self._next_post_id
        self._next_post_id += 1
        return id


class Post:
    def __init__(self, poster: Person, id: int, text: str) -> None:
        self._poster = poster
        self._id = id
        self._text = text
        self._liked_by = Set()

    @property
    def id(self) -> int:
        return self._id

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

    def __eq__(self, other) -> bool:
        return isinstance(other, Post) and other._poster == self._poster and other._id == self._id

    def __hash__(self) -> int:
        return hash(self._poster) * self._id

    def __repr__(self) -> str:
        return f"Post(poster={self._poster}, id={self._id}, text={self._text})"

    def _like(self, person: Person) -> None:
        self._liked_by.add(person)


class SocialNetwork:
    def __init__(self) -> None:
        self._people = SinglyLinkedList()

    @property
    def people(self) -> Iterator[Person]:
        return iter(self._people)

    @property
    def posts(self) -> Iterator[Post]:
        return chain.from_iterable(person.posts for person in self.people)

    def add_person(self, name) -> Person:
        person = Person(name)
        self._people.insert_last(person)
        return person
