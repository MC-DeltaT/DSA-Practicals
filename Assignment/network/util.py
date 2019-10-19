from .network import Person, Post, SocialNetwork
from dsa import Array, mergesort, Set

from typing import List


__all__ = [
    "people_by_popularity",
    "posts_by_popularity",
    "read_event_file",
    "read_network_file"
]


# Creates a network from a network file.
def read_network_file(file_path: str, **network_args) -> SocialNetwork:
    with open(file_path) as file:
        lines = file.readlines()

    # Note: allowed to use List for readlines().
    split_lines: Array[List[str]] = Array(len(lines))
    for i in range(len(split_lines)):
        line = lines[i].rstrip("\n")
        cols = line.split(":")
        if not line or len(cols) not in (1, 2):
            raise ValueError(f"line {i + 1} has invalid format.")
        split_lines[i] = cols

    # Pre-scan file to get number of people.
    names = Set()
    for i, columns in enumerate(split_lines, 1):
        if len(columns) == 1:
            name = columns[0]
            if not name or name.isspace():
                raise ValueError(f"line {i}: name cannot be blank or whitespace.")
            names.add(name)

    network_args["expected_people"] = len(names)
    network = SocialNetwork(**network_args)
    for name in names:
        network.add_person(name)

    for i, columns in enumerate(split_lines):
        if len(columns) == 2:
            try:
                person1 = network.find_person(columns[0])
                person2 = network.find_person(columns[1])
                person2.follow(person1)
            except ValueError as e:
                raise ValueError(f"line {i}: {e}")

    return network


# Reads an event file and applies the events to a network.
def read_event_file(file_path: str, network: SocialNetwork) -> None:
    with open(file_path) as file:
        for i, line in enumerate(file, 1):
            line = line.rstrip("\n")
            cols = line.split(":")
            if len(cols) == 2 and cols[0] in ("A", "a"):
                name = cols[1]
                if not name or name.isspace():
                    raise ValueError(f"line {i}: name cannot be blank or whitespace.")
                try:
                    network.add_person(name)
                except ValueError as e:
                    raise ValueError(f"line {i}: {e}")
            elif len(cols) == 2 and cols[0] in ("R", "r"):
                try:
                    network.delete_person(network.find_person(cols[1]))
                except ValueError as e:
                    raise ValueError(f"line {i}: {e}")
            elif len(cols) == 3 and cols[0] in ("F", "f"):
                try:
                    person1 = network.find_person(cols[1])
                    person2 = network.find_person(cols[2])
                    person2.follow(person1)
                except ValueError as e:
                    raise ValueError(f"line {i}: {e}")
            elif len(cols) == 3 and cols[0] in ("U", "u"):
                try:
                    person1 = network.find_person(cols[1])
                    person2 = network.find_person(cols[2])
                    person1.unfollow(person2)
                except ValueError as e:
                    raise ValueError(f"line {i}: {e}")
            elif len(cols) == 3 and cols[0] in ("P", "p"):
                try:
                    person = network.find_person(cols[1])
                    person.make_post(cols[2])
                except ValueError as e:
                    raise ValueError(f"line {i}: {e}")
            elif len(cols) == 4 and cols[0] in ("P", "p"):
                try:
                    clickbait_factor = int(cols[3])
                except ValueError:
                    raise ValueError(f"line {i}: invalid clickbait factor.")
                else:
                    try:
                        person = network.find_person(cols[1])
                        person.make_post(cols[2], clickbait_factor)
                    except ValueError as e:
                        raise ValueError(f"line {i}: {e}")
            else:
                raise ValueError(f"line {i} has invalid format.")


# Returns an array of a network's people sorted descending by follower count.
def people_by_popularity(network: SocialNetwork) -> Array[Person]:
    people = Array(network.people)
    # Mergesort to avoid slowdown of quicksort if many people have similar follower count.
    # (Which will happen as simulations progress.)
    mergesort(people, reverse=True, key=lambda p: p.follower_count)
    return people


# Returns an array of a network's posts sorted descending by like count.
def posts_by_popularity(network: SocialNetwork) -> Array[Post]:
    posts = Array(network.posts)
    # Mergesort to avoid slowdown of quicksort if many posts have similar like count.
    # (Which will happen as simulations progress.)
    mergesort(posts, reverse=True, key=lambda p: p.like_count)
    return posts
