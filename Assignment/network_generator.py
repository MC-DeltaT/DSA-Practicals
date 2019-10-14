# Generates randomised network and event files for the simulation mode.
# The follow and post counts for each person are normally distributed.
# Usage: python3 network_generator <person_count> <follows_mean> <follows_std> <posts_mean> <posts_std>
#   person_count: number of people in the network.
#   follows_mean: mean number of follows per person.
#   follows_std: standard deviation of number of follows per person.
#   posts_mean: mean of number of posts per person.
#   posts_std: standard deviation of number of posts per person.


import random
import sys


__all__ = [
    "generate_network"
]


def generate_network(person_count: int, follows_mean: float, follows_std: float, posts_mean: float, posts_std: float):
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

    with open("netfile_random.txt", "w") as file:
        people = range(1, person_count + 1)
        for person in people:
            file.write(f"{person}\n")

        for person1 in people:
            follow_count = max(0, min(person_count - 1, round(random.normalvariate(follows_mean, follows_std))))
            for person2 in random.sample(people, follow_count):
                if person1 != person2:
                    file.write(f"{person1}:{person2}\n")

    with open("eventfile_random.txt", "w") as file:
        for person in people:
            post_count = max(0, round(random.normalvariate(posts_mean, posts_std)))
            for i in range(post_count):
                file.write(f"P:{person}:post {i + 1}\n")


if __name__ == "__main__":
    valid = True
    if len(sys.argv) != 6:
        print("Usage: python3 network_generator <person_count> <follows_mean> <follows_std> <posts_mean> <posts_std>")
        valid = False

    if valid:
        try:
            person_count = int(sys.argv[1])
            follows_mean = float(sys.argv[2])
            follows_std = float(sys.argv[3])
            posts_mean = float(sys.argv[4])
            posts_std = float(sys.argv[5])
        except ValueError:
            print("Error: arguments have invalid type.")
            valid = False

    if valid:
        try:
            generate_network(person_count, follows_mean, follows_std, posts_mean, posts_std)
        except (ValueError, OSError) as e:
            print(f"Error: {e}")
