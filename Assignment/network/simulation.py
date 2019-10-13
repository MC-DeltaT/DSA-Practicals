from .network import Person, Post, SocialNetwork
from dsa import SinglyLinkedList

import random


__all__ = [
    "evolve_network"
]


# TODO: documentation.
def evolve_network(network: SocialNetwork, like_chance: float, follow_chance: float) -> None:
    def interact(person: Person, post: Post, new_follows: SinglyLinkedList[Person]) -> None:
        # Doesn't make sense for a person to interact with their own post via network evolution.
        if person is not post.poster:
            if random.random() < like_chance:
                try:
                    person.like_post(post)
                except ValueError:
                    # Ignore if the post has already been liked.
                    pass
                if random.random() < follow_chance:
                    new_follows.insert_last(post.poster)

    if not 0 <= like_chance <= 1.0:
        raise ValueError(f"like_chance must be in the range [0, 1], but got {like_chance}.")
    if not 0 <= follow_chance <= 1.0:
        raise ValueError(f"follow_chance must be in the range [0, 1], but got {follow_chance}.")

    for person in network.people:
        # Can't add to list of following while iterating following - will probably break something.
        # Keep track of additions and add later.
        new_follows: SinglyLinkedList[Person] = SinglyLinkedList()

        for following in person.following:
            for post in following.posts:
                interact(person, post, new_follows)

            for post in following.liked_posts:
                interact(person, post, new_follows)

        for person2 in new_follows:
            try:
                person.follow(person2)
            except ValueError:
                # Ignore if person is already following.
                pass
