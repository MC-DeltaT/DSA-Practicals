from common import unique_file
from network import evolve_network, people_by_popularity, Person, posts_by_popularity,\
    read_network_file, read_event_file, SocialNetwork

from contextlib import ExitStack
from itertools import takewhile
import sys
import time
from typing import Tuple


# If true, enables logging of network state and statistics each timestep.
# (Probably want this off if stat mode is enabled below.)
# TODO: set to true for submission.
LOGS_ENABLED = True

# If true, enables logging of additional network statistics for performance analysis.
# (Mainly for my own experimentation, feel free to ignore.)
# TODO: set to false for submission.
STATS_ENABLED = False


# Simulation mode entry point.
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


# Returns a network loaded from the network and event files specified in the command line.
def setup_network() -> SocialNetwork:
    network = None
    try:
        print("Reading network file... ", end="")
        network = read_network_file(sys.argv[2])
        print("done")
    except FileNotFoundError:
        print("Error: file not found.")
    except (OSError, ValueError) as e:
        print(f"Error: {e}")
    else:
        try:
            print("Reading event file... ", end="")
            read_event_file(sys.argv[3], network)
            print("done")
        except FileNotFoundError:
            print("Error: file not found.")
            network = None
        except (OSError, ValueError) as e:
            print(f"Error: {e}")
            network = None
    return network


# Runs the simulation to completion and logs each timestep if enabled.
def run_simulation(network: SocialNetwork, like_chance: float, follow_chance: float) -> None:
    print("Preliminary calculations... ", end="")
    annotate_solution(network)
    print("done")
    try:
        with ExitStack() as stack:
            if LOGS_ENABLED:
                output_file = stack.enter_context(unique_file("simulation", ".txt"))
            if STATS_ENABLED:
                stats_file = stack.enter_context(unique_file("stats", ".txt"))
                stats_file.write(f"{network.person_count} {like_chance} {follow_chance}\n")

            i = 1
            done = False
            while not done:
                print(f"Running timestep {i}... ", end="")

                start_time = time.perf_counter()
                new_likes, new_follows = evolve_network(network, like_chance, follow_chance)
                end_time = time.perf_counter()

                if LOGS_ENABLED:
                    log_timestep(network, i, output_file)

                if STATS_ENABLED:
                    like_completion, follow_completion = completion_analysis(network)
                    stats_file.write(f"{i} {end_time - start_time} {new_likes} {new_follows} {like_completion} {follow_completion}\n")
                    done = like_completion == 1 and follow_completion == 1
                else:
                    done = simulation_complete(network)

                i += 1
                print("done")
            print("Simulation complete.")
    except OSError as e:
        print(f"Error writing to output file: {e}")


# Writes people sorted by follower count, posts by like count, following list,
# and post like lists to the given file.
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
                new_likes = 0
                for p in person.posts:
                    if not hasattr(p, "_visited"):
                        new_likes += 1
                        p._visited = True
                likes += new_likes
                if new_likes > 0:
                    # People target_person is following will be counted separately,
                    # don't want to double up.
                    if not target_person.is_following(person):
                        following += 1
            # Don't need to inspect liked posts, since network always starts with no post likes.
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


# Returns a tuple of (like completion, follow completion) indicating the percentage of simulation
# completion for likes and follows.
# I.e gives the proportion of likes/follows that currently exist in the network out of all possible likes/follows.
# Only used if additional statistics are enabled.
def completion_analysis(network: SocialNetwork) -> Tuple[float, float]:
    actual_likes = 0
    actual_follows = 0
    max_likes = 0
    max_follows = 0
    for person in network.people:
        actual_likes += person.liked_post_count
        actual_follows += person.following_count
        max_likes += person._max_liked_posts
        max_follows += person._max_following
    return actual_likes / max_likes, actual_follows / max_follows
