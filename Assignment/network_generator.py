import random
from typing import Tuple


__all__ = [
    "linear_network",
    "random_network"
]


# Network with random follows and posts.
# The number of posts a person makes is normally distributed, with mean posts_mean and
# standard deviation posts_std.
# The number of follows a person makes is normally distributed with mean follows_mean and
# standard deviation follows_std. People to be followed are selected uniformly from all other people.
def random_network(person_count: int, follows_mean: float, follows_std: float,
                     posts_mean: float, posts_std: float) -> Tuple[str, str]:
    if person_count < 1:
        raise ValueError("Error: person_count must be >=1.")
    if follows_mean < 0:
        raise ValueError("Error: follows_mean must be >=0.")
    if follows_std <= 0:
        raise ValueError("Error: follows_std must be >0.")
    if posts_mean < 0:
        raise ValueError("Error: posts_mean must be >=0.")
    if posts_std <= 0:
        raise ValueError("Error: posts_std must be >0.")

    netfile = ""
    people = range(1, person_count + 1)
    for person in people:
        netfile += f"{person}\n"

    for person1 in people:
        follow_count = max(0, min(person_count - 1, round(random.normalvariate(follows_mean, follows_std))))
        for person2 in random.sample(people, follow_count):
            if person1 != person2:
                netfile += f"{person1}:{person2}\n"

    eventfile = ""
    for person in people:
        post_count = max(0, round(random.normalvariate(posts_mean, posts_std)))
        for i in range(post_count):
            eventfile += f"P:{person}:post {i + 1}\n"

    return netfile, eventfile


# Network resembling a linked list.
# Person 0 follows person 1, person 1 follows person 2, etc.
# Person N has a single post.
def linear_network(person_count: int) -> Tuple[str, str]:
    if person_count < 1:
        raise ValueError("Error: person_count must be >=1.")

    netfile = ""
    people = range(1, person_count + 1)
    for person in people:
        netfile += f"{person}\n"

    person1 = people[0]
    for person2 in people[1:]:
        netfile += f"{person2}:{person1}\n"
        person1 = person2

    eventfile = f"P:{people[-1]}:post 0\n"

    return netfile, eventfile
