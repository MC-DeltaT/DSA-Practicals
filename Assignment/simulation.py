from network import Person, Post, SocialNetwork

import random


# TODO: documentation.
def evolve_network(network: SocialNetwork, like_chance: float, follow_chance: float) -> None:
    def interact(person: Person, post: Post) -> None:
        if random.random() < like_chance:
            try:
                person.like_post(post)
            except ValueError:
                # Ignore if the post has already been liked.
                pass
            else:
                if random.random() < follow_chance:
                    try:
                        person.follow(post.poster)
                    except ValueError:
                        # Ignore if poster is already being followed.
                        pass

    if not 0 <= like_chance <= 1.0:
        raise ValueError(f"like_chance must be in the range [0, 1], but got {like_chance}.")
    if not 0 <= follow_chance <= 1.0:
        raise ValueError(f"follow_chance must be in the range [0, 1], but got {follow_chance}.")

    for person in network.people:
        for following in person.following:
            for post in following.posts:
                interact(person, post)

            for post in following.liked_posts:
                interact(person, post)
