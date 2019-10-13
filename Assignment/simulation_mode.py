from dsa import Set
from network import evolve_network, people_by_popularity, Person, posts_by_popularity,\
    read_network_file, read_event_file, SocialNetwork

from itertools import takewhile
import sys
import time
from typing import Tuple


def main() -> None:
    like_chance, follow_chance = get_probabilities()
    valid = None not in (like_chance, follow_chance)

    if valid:
        network = setup_network()
        valid = network is not None

    if valid:
        run_simulation(network, like_chance, follow_chance)


# Parses a tuple of the (like chance, follow chance) from the command line arguments.
# If either is invalid, prints errors to the terminal and returns None.
def get_probabilities() -> Tuple[float, float]:
    like_probability = None
    try:
        like_probability = float(sys.argv[4])
    except ValueError:
        print("Error: like_prob must be a real number.")
    else:
        if not 0 <= like_probability <= 1:
            print("Error: like_prob must be >=0 and <=1.")
            like_probability = None

    follow_probability = None
    try:
        follow_probability = float(sys.argv[5])
    except ValueError:
        print("Error: follow_prob must be a real number.")
    else:
        if not 0 <= follow_probability <= 1:
            print("Error: follow_prob must be >=0 and <=1.")
            like_probability = None

    return like_probability, follow_probability


def setup_network() -> SocialNetwork:
    network = None
    try:
        network = read_network_file(sys.argv[2])
    except FileNotFoundError:
        print("Error: network file not found.")
    except (OSError, ValueError) as e:
        print(f"Error reading network file: {e}")
    else:
        try:
            read_event_file(sys.argv[3], network)
        except FileNotFoundError:
            print("Error: event file not found.")
            network = None
        except (OSError, ValueError) as e:
            print(f"Error reading event file: {e}")
            network = None
    return network


def run_simulation(network: SocialNetwork, like_chance: float, follow_chance: float) -> None:
    try:
        with open(f"simulation_{round(time.time())}.txt", "w") as output_file:
            i = 1
            # TODO? completion detection.
            while i <= 20: #not simulation_complete(network):
                print(f"Timestep {i}")
                evolve_network(network, like_chance, follow_chance)
                log_timestep(network, i, output_file)
                i += 1
    except OSError as e:
        print(f"Error writing to output file: {e}")


def log_timestep(network: SocialNetwork, timestep: int, file) -> None:
    file.write(f"Timestep {timestep}\n")

    file.write("  People by popularity:\n")
    for person in people_by_popularity(network):
        file.write(f"    {person.follower_count} followers : {person}\n")

    file.write("  Posts by popularity:\n")
    for post in posts_by_popularity(network):
        file.write(f"    {post.like_count} likes : {post}\n")

    file.write("  Following:\n")
    for person in network.people:
        following_str = ", ".join(map(str, person.following))
        file.write(f"    {person} : {following_str}\n")

    file.write("  Post likes:\n")
    for post in network.posts:
        likers_str = ", ".join(map(str, post.likers))
        file.write(f"    {post} : {likers_str}\n")

    file.write("\n")


# TODO?
# def simulation_complete(network: SocialNetwork) -> bool:
#     def _connected(person: Person) -> Set[Person]:
#         def __connected(person: Person, connected: Set[Person]) -> None:
#             connected.add(person)
#             for p in person.following:
#                 if connected.add(p):
#                     __connected(p, connected)
#                 for post in p.liked_posts:
#                     if connected.add(post.poster):
#                         __connected(post.poster, connected)
#
#         connected = Set(network._expected_people)
#         __connected(person, connected)
#         return connected
#
#     saturated = True
#     for person in takewhile(lambda _: saturated, network.people):
#         if person.following_count < len(_connected(person)) - 1:
#             saturated = False
#     return saturated
