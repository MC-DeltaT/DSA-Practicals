from network import SocialNetwork

import random


# TODO: documentation.
def evolve_network(network: SocialNetwork, like_chance: float, follow_chance: float) -> None:
    if not 0 <= like_chance <= 1.0:
        raise ValueError(f"like_chance must be in the range [0, 1], but got {like_chance}.")
    if not 0 <= follow_chance <= 1.0:
        raise ValueError(f"follow_chance must be in the range [0, 1], but got {follow_chance}.")

    for person in network.people:
        for following in person.following:
            # Possibility to like post made by following.
            for post in following.posts:
                r = random.random()
                if r < like_chance:
                    try:
                        person.like_post(post.id)
                    except ValueError:
                        # Ignore if the post has already been liked.
                        pass
                    else:
                        try:
                            person.follow(post.poster)
                        except ValueError:
                            # Ignore if poster is already being followed.
                            pass

            # Possibility to like post liked by following.
            for post in following.liked_posts:
                r = random.random()
                if r < like_chance:
                    try:
                        person.like_post(post.id)
                    except ValueError:
                        # Ignore if the post has already been liked.
                        pass
                    else:
                        try:
                            person.follow(post.poster)
                        except ValueError:
                            # Ignore if poster is already being followed.
                            pass
