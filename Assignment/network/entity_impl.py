from .entity import Entity, Person, Post

from typing import Iterator


# Stores an entity's actual data in the graph.
# (Used as the value attribute of the GraphVertex.)
class EntityData:
    def __init__(self, guid: int) -> None:
        self.guid = guid


class PersonData(EntityData):
    def __init__(self, id: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.id = id


class PostData(EntityData):
    def __init__(self, id: int, poster_id: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.id = id
        self.poster_id = poster_id


# Represents an entity in the network that external code gets to use.
# Binds the entity's operations with its actual data.
class EntityImpl(Entity):
    def __init__(self, data: EntityData, network) -> None:
        self._data = data
        self._network = network

    @property
    def guid(self) -> int:
        return self._data.guid


class PersonImpl(Person, EntityImpl):
    # Static type checker hint.
    _data: PersonData

    @property
    def id(self) -> int:
        return self._data.id

    @property
    def followers(self) -> Iterator[Person]:
        return self._network.get_followers(self.guid)

    @property
    def following(self) -> Iterator[Person]:
        return self._network.get_following(self.guid)

    @property
    def posts(self) -> Iterator[Post]:
        return self._network.get_posts(self.guid)

    @property
    def liked_posts(self) -> Iterator[Post]:
        return self._network.get_liked_posts(self.guid)

    def follow(self, person: int) -> None:
        self._network.follow(self.guid, person)

    def make_post(self) -> None:
        self._network.make_post(self.guid)

    def like_post(self, post: int) -> None:
        self._network.like_post(self.guid, post)


class PostImpl(Post, EntityImpl):
    # Static type checker hint.
    _data: PostData

    @property
    def id(self) -> int:
        return self._data.id

    @property
    def poster(self) -> Person:
        return self._network.get_post(self._data.poster_id)

    @property
    def liked_by(self) -> Iterator[Person]:
        return self._network.get_liked_by(self.guid)
