from .network import Person, Post, SocialNetwork
from dsa import Array, quicksort, Set

from typing import List


__all__ = [
    "people_by_popularity",
    "posts_by_popularity",
    "read_event_file",
    "read_network_file",
]


# Creates a network from a network file.
def read_network_file(file_path: str) -> SocialNetwork:
    with open(file_path) as file:
        lines = file.readlines()

    # Note: allowed to use List for readlines().
    split_lines: Array[List[str]] = Array(len(lines))
    for i in range(len(split_lines)):
        cols = lines[i].rstrip("\n").split(":")
        if len(cols) not in (1, 2):
            raise ValueError(f"line {i + 1} is invalid.")
        split_lines[i] = cols

    # Pre-scan file to get number of people.
    names = Set()
    for columns in split_lines:
        # Allow follow specification ("name1:name2") to "declare" both people.
        for name in columns:
            names.add(name)

    # Can't really predict number of posts so just guess 10 posts per person.
    network = SocialNetwork(len(names), 10 * len(names))
    for name in names:
        network.add_person(name)

    # Terrible O(n^2) algorithm here, but probably no one's gonna input a huge file.
    for person in network.people:
        for i, columns in enumerate(split_lines):
            if len(columns) == 2 and columns[0] == person.name:
                person.follow(network.find_person(columns[1]))

    return network


# Reads an event file and applies the events to a network.
def read_event_file(file_path: str, network: SocialNetwork) -> None:
    # TODO
    ...


# Returns an array of a network's people sorted descending by follower count.
def people_by_popularity(network: SocialNetwork) -> Array[Person]:
    people = Array(network.people)
    quicksort(people, reverse=True, key=lambda p: p.follower_count)
    return people


# Returns an array of a network's posts sorted descending by like count.
def posts_by_popularity(network: SocialNetwork) -> Array[Post]:
    posts = Array(network.posts)
    quicksort(posts, reverse=True, key=lambda p: p.like_count)
    return posts
