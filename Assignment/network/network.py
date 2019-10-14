from common import SizedIterable, str_hash
from dsa import HashTable, Set, SinglyLinkedList

from itertools import chain


__all__ = [
    "Person",
    "Post",
    "SocialNetwork"
]


class Person:
    def __init__(self, name: str, network: "SocialNetwork") -> None:
        self._name = name
        self._network = network
        self._posts: SinglyLinkedList["Post"] = SinglyLinkedList()
        self._followers: Set["Person"] = Set(network._expected_people)
        self._following: Set["Person"] = Set(network._expected_people)
        self._liked_posts: Set["Post"] = Set(network._expected_posts)
        self._post_id = 1

    @property
    def name(self) -> str:
        return self._name

    # Posts are ordered most recent first.
    @property
    def posts(self) -> SizedIterable["Post"]:
        return SizedIterable(self._posts, self.post_count)

    @property
    def followers(self) -> SizedIterable["Person"]:
        return SizedIterable(self._followers, self.follower_count)

    @property
    def following(self) -> SizedIterable["Person"]:
        return SizedIterable(self._following, self.following_count)

    @property
    def liked_posts(self) -> SizedIterable["Post"]:
        return SizedIterable(self._liked_posts, self.liked_post_count)

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
        post = Post(self, self._post_id, text)
        self._post_id += 1
        self._posts.insert_first(post)
        return post

    def follow(self, person: "Person") -> None:
        if person is self:
            raise ValueError(f"Cannot follow self.")
        if not self._following.add(person):
            raise ValueError(f"{person} already follows {self}.")
        assert person._followers.add(self)

    def unfollow(self, person: "Person") -> None:
        try:
            self._following.remove(person)
            person._followers.remove(self)
        except KeyError:
            raise ValueError(f"{self} doesn't follow {person}")

    def like_post(self, post: "Post") -> None:
        if not self._liked_posts.add(post):
            raise ValueError(f"{self} already likes {post}.")
        post._liked_by.add(self)

    def unlike_post(self, post: "Post") -> None:
        try:
            self._liked_posts.remove(post)
            post._liked_by.remove(self)
        except KeyError:
            raise ValueError(f"{self} doesn't like {post}")

    def is_following(self, person: "Person") -> bool:
        return person in self._following

    def is_followed_by(self, person: "Person") -> bool:
        return person in self._followers

    def likes_post(self, post: "Post") -> bool:
        return post in self._liked_posts

    def __eq__(self, other) -> bool:
        return isinstance(other, Person) and other._name == self._name

    def __hash__(self) -> int:
        return str_hash(self._name)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Person(name={self._name})"

    def _delete(self) -> None:
        # Set attributes to None for debugging purposes and to make sure GC collects everything.

        for person in self._following:
            person._followers.remove(self)
        self._following = None

        for person in self._followers:
            person._following.remove(self)
        self._followers = None

        for post in self._liked_posts:
            post._liked_by.remove(self)
        self._liked_posts = None

        for post in self._posts:
            post._delete()
        self._posts = None

        self._network = None
        self._name = "[DELETED]"


class Post:
    def __init__(self, poster: Person, id: int, text: str) -> None:
        self._poster = poster
        self._id = id
        self._text = text
        self._liked_by: Set[Person] = Set(self._poster._network._expected_people)
        self._poster._network._post_count += 1

    @property
    def poster(self) -> Person:
        return self._poster

    @property
    def text(self) -> str:
        return self._text

    # Abbreviated version of the post text.
    @property
    def short_text(self) -> str:
        if len(self._text) > 30:
            res = self._text[:27] + "..."
        else:
            res = self._text
        return res

    @property
    def likers(self) -> SizedIterable[Person]:
        return SizedIterable(self._liked_by, self.like_count)

    @property
    def like_count(self) -> int:
        return len(self._liked_by)

    def is_liked_by(self, person: Person) -> bool:
        return person in self._liked_by

    def __eq__(self, other) -> bool:
        # Note: posts with the same text are not necessarily the same post!
        return isinstance(other, Post) and other._poster == self._poster and other._id == self._id

    def __hash__(self) -> int:
        # Hopefully this doesn't collide often.
        return hash(self._poster) + str_hash(self._text) + self._id

    def __str__(self) -> str:
        # In most cases probably don't want to see full text (could be very long).
        return f"{self.poster.name}: {self.short_text}"

    def __repr__(self) -> str:
        return f"Post(poster={self._poster}, id={self._id}, text={self._text})"

    def _delete(self) -> None:
        for person in self._liked_by:
            person._liked_posts.remove(self)
        self._poster._network._post_count -= 1
        self._liked_by = None
        self._poster = None
        self._text = None
        # Responsibility of caller to remove this object from poster's list of posts.


class SocialNetwork:
    # expected_people: expected total number of people to be present in the network.
    # expected_post: expected total number of posts to be present in the network.
    # (These are solely for performance optimisation.)
    def __init__(self, expected_people: int, expected_posts: int) -> None:
        self._people: HashTable[str, Person] = HashTable(expected_people)
        self._post_count = 0
        self._expected_people = max(expected_people, 1)
        self._expected_posts = max(expected_posts, 1)

    @property
    def person_count(self) -> int:
        return len(self._people)

    @property
    def people(self) -> SizedIterable[Person]:
        return SizedIterable(self._people.values(), self.person_count)

    @property
    def posts(self) -> SizedIterable[Post]:
        iterator = chain.from_iterable(person.posts for person in self.people)
        return SizedIterable(iterator, self.post_count)

    @property
    def post_count(self) -> int:
        return self._post_count

    def add_person(self, name) -> Person:
        if name in self._people:
            raise ValueError(f'Person with name "{name}" already exists in network.')
        person = Person(name, self)
        self._people[name] = person
        return person

    def delete_person(self, person: Person) -> None:
        del self._people[person.name]
        person._delete()

    def find_person(self, name: str) -> Person:
        try:
            return self._people[name]
        except KeyError:
            raise ValueError(f'Person with name "{name}" doesn\'t exist in network.')
