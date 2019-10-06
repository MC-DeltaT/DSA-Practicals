from .entity import Person, Post
from .entity_impl import PersonData, PersonImpl, PostData, PostImpl
from dsa import Graph

from enum import Enum
from typing import Iterator


__all__ = [
    "Person",
    "Post",
    "SocialNetwork"
]


class SocialNetwork:
    def __init__(self) -> None:
        self._graph = Graph()
        self._next_guid = 1
        self._next_person_id = 1
        self._next_post_id = 1

    @property
    def person_ids(self) -> Iterator[int]:
        return map(lambda person: person.id, self.people)

    @property
    def post_ids(self) -> Iterator[int]:
        return map(lambda post: post.id, self.posts)

    @property
    def people(self) -> Iterator[Person]:
        return map(lambda vertex: PersonImpl(vertex.value, self),
                   filter(lambda vertex: isinstance(vertex.value, PersonData),
                          self._graph.vertices))

    @property
    def posts(self) -> Iterator[Post]:
        return map(lambda vertex: PostImpl(vertex.value, self),
                   filter(lambda vertex: isinstance(vertex.value, PostData),
                          self._graph.vertices))

    # Adds a new person to the network and returns their ID.
    def add_person(self) -> int:
        guid = self._generate_guid()
        person_id = self._generate_person_id()
        person_data = PersonData(id=person_id, guid=guid)
        self._graph.add_vertex(person_id, person_data)
        return person_id

    def make_post(self, person: int) -> int:
        guid = self._generate_guid()
        post_id = self._generate_post_id()
        post_data = PostData(id=post_id, poster_id=person, guid=guid)
        self._graph.add_vertex(post_id, post_data)
        self._graph.add_edge(person, post_id, _EdgeType.POSTED)
        self._graph.add_edge(post_id, person, _EdgeType.POSTED_BY)
        return post_id

    def get_person(self, id: int) -> Person:
        data = self._graph.get_vertex(id).value
        return PersonImpl(data, self)

    def get_post(self, id: int) -> Post:
        data = self._graph.get_vertex(id).value
        return PostImpl(data, self)

    # Sets person with id1 to be following person with id2.
    def follow(self, id1: int, id2: int) -> None:
        self._graph.add_edge(id1, id2, _EdgeType.FOLLOWING)
        self._graph.add_edge(id2, id1, _EdgeType.FOLLOWED_BY)

    def like_post(self, person: int, post: int) -> None:
        self._graph.add_edge(person, post, _EdgeType.LIKES)
        self._graph.add_edge(post, person, _EdgeType.LIKED_BY)

    def get_followers(self, person: int) -> Iterator[Person]:
        return map(lambda edge: PersonImpl(edge.sink.value, self),
                   filter(lambda edge: edge.label == _EdgeType.FOLLOWED_BY,
                          self._graph.get_out_edges(person)))

    def get_following(self, person: int) -> Iterator[Person]:
        return map(lambda edge: PersonImpl(edge.sink.value, self),
                   filter(lambda edge: edge.label == _EdgeType.FOLLOWING,
                          self._graph.get_out_edges(person)))

    def get_posts(self, person: int) -> Iterator[Post]:
        return map(lambda edge: PostImpl(edge.sink.value, self),
                   filter(lambda edge: edge.label == _EdgeType.POSTED,
                          self._graph.get_out_edges(person)))

    def get_liked_posts(self, person: int) -> Iterator[Post]:
        return map(lambda edge: PostImpl(edge.sink.value, self),
                   filter(lambda edge: edge.label == _EdgeType.LIKES,
                          self._graph.get_out_edges(person)))

    def get_liked_by(self, post: int) -> Iterator[Person]:
        return map(lambda edge: PersonImpl(edge.sink.value, self),
                   filter(lambda edge: edge.label == _EdgeType.LIKED_BY,
                          self._graph.get_out_edges(post)))

    # Creates unique global IDs for entities in this network.
    def _generate_guid(self) -> int:
        id = self._next_guid
        self._next_guid += 1
        return id

    # Creates IDs that are unique within people.
    def _generate_person_id(self) -> int:
        id = self._next_person_id
        self._next_person_id += 1
        return id

    # Creates IDs that are unique within posts.
    def _generate_post_id(self) -> int:
        id = self._next_post_id
        self._next_post_id += 1
        return id


# Describes the relationship from a source node to a sink node in the network graph.
class _EdgeType(Enum):
    # Person -> Person
    FOLLOWING = 1
    FOLLOWED_BY = 2

    # Person -> Post
    LIKES = 3
    POSTED = 4

    # Post -> Person
    LIKED_BY = 5
    POSTED_BY = 6
