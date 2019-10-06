from abc import ABC, abstractmethod
from typing import Iterator


__all__ = [
    "Entity",
    "Person",
    "Post"
]

# TODO: explicit ID types.
# class EntityID:
#     def __init__(self, value: int) -> None:
#         self._value = value
#
#     @property
#     def value(self) -> int:
#         return self._value
#
#     def __eq__(self, other) -> bool:
#         return type(self) == type(other) and other.value == self.value
#
#     def __str__(self) -> str:
#         return str(self.value)
#
#     def __repr__(self) -> str:
#         return f"{self.__class__}(value={self._value})"
#
#
# class PersonID(EntityID):
#     pass
#
#
# class PostID(EntityID):
#     pass


class Entity(ABC):
    @property
    @abstractmethod
    def guid(self) -> int:
        pass


class Person(Entity, ABC):
    @property
    @abstractmethod
    def id(self) -> int:
        pass

    @property
    @abstractmethod
    def followers(self) -> Iterator["Person"]:
        pass

    @property
    @abstractmethod
    def following(self) -> Iterator["Person"]:
        pass

    @property
    @abstractmethod
    def posts(self) -> Iterator["Post"]:
        pass

    @property
    @abstractmethod
    def liked_posts(self) -> Iterator["Post"]:
        pass

    @abstractmethod
    def follow(self, person) -> None:
        pass

    @abstractmethod
    def make_post(self) -> None:
        pass

    @abstractmethod
    def like_post(self, post) -> None:
        pass

    def __str__(self) -> str:
        return f"Person {self.id}"


class Post(Entity, ABC):
    @property
    @abstractmethod
    def id(self) -> int:
        pass

    @property
    @abstractmethod
    def poster(self) -> Person:
        pass

    @property
    @abstractmethod
    def liked_by(self) -> Iterator[Person]:
        pass

    def __str__(self) -> str:
        return f"Post {self.id}"
