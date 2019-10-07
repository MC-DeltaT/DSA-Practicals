from dsa import LinkedList

from itertools import chain
from typing import Iterator


__all__ = [
    "Person",
    "Post",
    "SocialNetwork"
]


class Person:
    def __init__(self, id: int) -> None:
        self._id = id
        self._posts = LinkedList()
        self._followers = LinkedList()
        self._following = LinkedList()
        self._liked_posts = LinkedList()
        self._next_post_id = 1

    @property
    def id(self) -> int:
        return self._id

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

    def make_post(self) -> "Post":
        id = self._generate_post_id()
        post = Post(self, id=id)
        self._posts.insert_last(post)
        return post

    def follow(self, person: "Person") -> None:
        if self.is_followed_by(person):
            raise ValueError(f"{person} already follows {self}.")
        self._following.insert_last(person)
        person._followers.insert_last(self)

    def like_post(self, post: "Post") -> None:
        if self.likes_post(post):
            raise ValueError(f"{self} already likes {post}.")
        self._liked_posts.insert_last(post)
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
    def __init__(self, poster: Person, id: int) -> None:
        self._poster = poster
        self._id = id
        self._liked_by = LinkedList()

    @property
    def id(self) -> int:
        return self.id

    @property
    def poster(self) -> Person:
        return self._poster

    @property
    def likers(self) -> Iterator[Person]:
        return iter(self._liked_by)

    def is_liked_by(self, person: Person) -> bool:
        return person in self._liked_by

    def __eq__(self, other) -> bool:
        return isinstance(other, Post) and other.poster == self.poster and other.id == self.id

    def __str__(self) -> str:
        return f"Post {self.id} from person {self.poster.id}"

    def __repr__(self) -> str:
        return f"Post(poster={self._poster}, id={self._id})"

    def _like(self, person: Person) -> None:
        self._liked_by.insert_last(person)


class SocialNetwork:
    def __init__(self) -> None:
        self._people = LinkedList()
        self._next_person_id = 1

    @property
    def people(self) -> Iterator[Person]:
        return iter(self._people)

    @property
    def posts(self) -> Iterator[Post]:
        return chain.from_iterable(person.posts for person in self.people)

    def add_person(self) -> Person:
        id = self._generate_person_id()
        person = Person(id=id)
        self._people.insert_last(person)
        return person

    # Creates IDs that are unique within Person objects in this network.
    def _generate_person_id(self) -> int:
        id = self._next_person_id
        self._next_person_id += 1
        return id
