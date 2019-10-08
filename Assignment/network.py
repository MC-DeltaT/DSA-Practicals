from dsa import Set

from itertools import chain
from typing import Iterator


__all__ = [
    "Person",
    "Post",
    "SocialNetwork"
]


class Person:
    def __init__(self, id: int, name: str) -> None:
        self._id = id
        self._name = name
        self._posts = Set()
        self._followers = Set()
        self._following = Set()
        self._liked_posts = Set()
        self._next_post_id = 1

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

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

    def make_post(self, text: str) -> "Post":
        id = self._generate_post_id()
        post = Post(self, id, text)
        self._posts.add(post)
        return post

    def follow(self, person: "Person") -> None:
        if self.is_followed_by(person):
            raise ValueError(f"{person} already follows {self}.")
        self._following.add(person)
        person._followers.add(self)

    def like_post(self, post: "Post") -> None:
        if self.likes_post(post):
            raise ValueError(f"{self} already likes {post}.")
        self._liked_posts.add(post)
        post._like(self)

    def is_following(self, person: "Person") -> bool:
        return person in self._following

    def is_followed_by(self, person: "Person") -> bool:
        return person in self._followers

    def likes_post(self, post: "Post") -> bool:
        return post in self._liked_posts

    def __str__(self) -> str:
        return f"Person {self.id}"

    def __repr__(self) -> str:
        return f"Person(id={self._id})"

    def __eq__(self, other) -> bool:
        return isinstance(other, Person) and other.id == self.id

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
        return self.id

    @property
    def poster(self) -> Person:
        return self._poster

    @property
    def text(self) -> str:
        return self._text

    @property
    def likers(self) -> Iterator[Person]:
        return iter(self._liked_by)

    def is_liked_by(self, person: Person) -> bool:
        return person in self._liked_by

    def __eq__(self, other) -> bool:
        return isinstance(other, Post) and other.poster == self.poster and other.id == self.id

    def __str__(self) -> str:
        return f"Post {self.id} from {self.poster}"

    def __repr__(self) -> str:
        return f"Post(poster={self._poster}, id={self._id}, text={self._text})"

    def _like(self, person: Person) -> None:
        self._liked_by.add(person)


class SocialNetwork:
    def __init__(self) -> None:
        self._people = Set()
        self._next_person_id = 1

    @property
    def people(self) -> Iterator[Person]:
        return iter(self._people)

    @property
    def posts(self) -> Iterator[Post]:
        return chain.from_iterable(person.posts for person in self.people)

    def add_person(self, name) -> Person:
        id = self._generate_person_id()
        person = Person(id, name)
        self._people.add(person)
        return person

    # Creates IDs that are unique within Person objects in this network.
    def _generate_person_id(self) -> int:
        id = self._next_person_id
        self._next_person_id += 1
        return id
