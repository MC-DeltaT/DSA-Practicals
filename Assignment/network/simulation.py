from .network import Person, Post, SocialNetwork
from dsa import Array, SinglyLinkedList

import random
from typing import Tuple


__all__ = [
    "evolve_network"
]


# Evolves a network with the following rules:
#   Each person "interacts" with the posts and liked posts of people they follow.
#   For each post interacted with, there is a like_chance chance of the person liking that post,
#   enhanced by the posts' clickbait factor.
#   If the person likes the post, then there is a follow_chance chance of the person following the post's creator.
# Returns a tuple of (total new likes, total new follows)
def evolve_network(network: SocialNetwork, like_chance: float, follow_chance: float) -> Tuple[int, int]:
    def interact(person: Person, post: Post, new_likes: SinglyLinkedList[Post],
                 new_follows: SinglyLinkedList[Person]) -> None:
        # Doesn't make sense for a person to interact with their own post via network evolution.
        # Can use object identity since people are always unique within 1 instance of the application.
        if person is not post.poster:
            if random.random() <= like_chance * post.clickbait_factor:
                new_likes.insert_last(post)
                if random.random() <= follow_chance:
                    new_follows.insert_last(post.poster)

    if not 0 <= like_chance <= 1.0:
        raise ValueError(f"like_chance must be in the range [0, 1], but got {like_chance}.")
    if not 0 <= follow_chance <= 1.0:
        raise ValueError(f"follow_chance must be in the range [0, 1], but got {follow_chance}.")

    # Don't want to actually change the network during an update, as that could change the outcome.
    # Therefore keep track of any new likes and follows and apply them all at the end.
    changes = Array(network.person_count)

    for i, person in enumerate(network.people):
        new_likes: SinglyLinkedList[Post] = SinglyLinkedList()
        new_follows: SinglyLinkedList[Person] = SinglyLinkedList()
        for following in person.following:
            for post in following.posts:
                # Mark the post so it isn't interacted with again in this timestep by this person.
                if post.__dict__.get("_last_interaction") is not person:
                    interact(person, post, new_likes, new_follows)
                    post._last_interaction = person
            for post in following.liked_posts:
                if post.__dict__.get("_last_interaction") is not person:
                    interact(person, post, new_likes, new_follows)
                    post._last_interaction = person
        changes[i] = (person, new_likes, new_follows)

    new_like_count = 0
    new_follow_count = 0
    for person, new_likes, new_follows in changes:
        for post in new_likes:
            try:
                person.like_post(post)
            except ValueError:
                # Ignore if post is already liked.
                pass
            else:
                new_like_count += 1

        for person2 in new_follows:
            try:
                person.follow(person2)
            except ValueError:
                # Ignore if person is already following.
                pass
            else:
                new_follow_count += 1

    for post in network.posts:
        try:
            delattr(post, "_last_interaction")
        except AttributeError:
            pass

    return new_like_count, new_follow_count
