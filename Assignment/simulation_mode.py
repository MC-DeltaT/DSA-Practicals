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
    annotate_solution(network)
    try:
        with open(f"simulation_{round(time.time())}.txt", "w") as output_file:
            i = 1
            while not simulation_complete(network):
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


# The entire simulation can actually be solved instantly via a series of
# depth-first searches. So we can "solve" it once at the start and then keep
# that info around to check when the full simulation is complete.
def annotate_solution(network: SocialNetwork) -> None:
    # Counts the maximum number of liked posts and following people obtainable via network simulation.
    def possible_connections(network: SocialNetwork, person: Person) -> Tuple[int, int]:
        # Effectively a depth-first search, following only edges that represent
        # "follows person" and "likes post".
        def _possible_connections(target_person: Person, person: Person,
                                  likes: int, following: int) -> Tuple[int, int]:
            person._visited = True
            if person is not target_person:
                for p in person.posts:
                    if not hasattr(p, "_visited"):
                        likes += 1
                        # People target_person is following will be counted separately,
                        # don't want to double up.
                        if not target_person.is_following(p.poster):
                            following += 1
                        p._visited = True
            for p in person.liked_posts:
                if p.poster is not target_person:
                    if not hasattr(p, "_visited"):
                        likes += 1
                        if not target_person.is_following(p.poster):
                            following += 1
                        p._visited = True
            for p in person.following:
                if not hasattr(p, "_visited"):
                    # Network probably won't be enormous, so recursion should be ok.
                    # Can easily change if not the case.
                    likes, following = _possible_connections(target_person, p, likes, following)
            return likes, following

        likes, following = _possible_connections(person, person, 0, person.following_count)
        for person in network.people:
            try:
                del person._visited
            except AttributeError:
                pass
            for post in person.posts:
                try:
                    del post._visited
                except AttributeError:
                    pass
        return likes, following

    for person in network.people:
        person._max_liked_posts, person._max_following = possible_connections(network, person)


# Checks if the network has evolved to a state where it will not evolve any further,
# i.e. when everyone is following everyone they can, and everyone likes every post they can.
def simulation_complete(network: SocialNetwork) -> bool:
    saturated = True
    for person in takewhile(lambda _: saturated, network.people):
        if person.following_count < person._max_following:
            saturated = False
        elif person.liked_post_count < person._max_liked_posts:
            saturated = False
    return saturated
