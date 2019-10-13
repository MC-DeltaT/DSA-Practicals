from network import evolve_network, Person, people_by_popularity, posts_by_popularity,\
    read_network_file, SocialNetwork

import pickle
from typing import Optional, Tuple


def main() -> None:
    network = None
    like_chance = None
    follow_chance = None

    selection = None
    while selection is None or selection != 11:
        print("Main menu:")
        print("  1) Load network from network file")
        print("  2) Load network from serialised")
        print("  3) Set probabilities")
        print("  4) Add person")
        print("  5) View person (and operations)")
        print("  6) Display network")
        print("  7) Display statistics")
        print("  8) Evolve network")
        print("  9) Save network to network file")
        print("  10) Save network to serialised")
        print("  11) Exit application")
        print()

        selection = None
        while selection is None:
            selection = input("Enter an option: ")
            try:
                selection = int(selection)
            except ValueError:
                print("Error: selection must be an integer.")
                selection = None
            else:
                if not 1 <= selection <= 11:
                    print(f"Error: selection must be >=1 and <=11.")
                    selection = None

        print()
        if selection == 1:
            network = load_network()
        elif selection == 2:
            network = load_network_serialised()
        elif selection == 3:
            like_chance, follow_chance = set_probabilities()
        elif selection == 4:
            add_person(network)
        elif selection == 5:
            inspect_person(network)
        elif selection == 6:
            display_network(network)
        elif selection == 7:
            network_statistics(network)
        elif selection == 8:
            run_timestep(network, like_chance, follow_chance)
        elif selection == 9:
            save_network(network)
        elif selection == 10:
            save_network_serialised(network)
        elif selection == 11:
            print("Exiting.")
        print()


def load_network() -> SocialNetwork:
    path = input("Enter network file path: ")
    try:
        network = read_network_file(path)
    except FileNotFoundError:
        print("Error: file not found.")
        network = None
    except (OSError, ValueError) as e:
        print(f"Error reading network file: {e}")
        network = None
    return network


def load_network_serialised() -> SocialNetwork:
    path = input("Enter serialised file path: ")
    network = None
    try:
        with open(path, "rb") as file:
            network = pickle.load(file)
    except FileNotFoundError:
        print("Error: file not found.")
    except OSError as e:
        print(f"Error reading from file: {e.strerror}")
    # Yes catching base Exception is bad, except the Python docs, in their infinite wisdom,
    # don't actually say which exceptions pickle.load() can raise.
    except Exception as e:
        print(f"Error reading serialised file: {e}")
    else:
        if not isinstance(network, SocialNetwork):
            print("Error: serialised file does not contain a network.")
            network = None
    return network


def set_probabilities() -> Tuple[float, float]:
    def _get_probability(name: str) -> float:
        probability = None
        while probability is None:
            probability = input(f"Enter {name} (0-1): ")
            try:
                probability = float(probability)
            except ValueError:
                print(f"Error: {name} must be a real number.")
                probability = None
            else:
                if not 0 <= probability <= 1:
                    print(f"Error: {name} must be >=0 and <= 1.")
                    probability = None
        return probability

    like_chance = _get_probability("like chance")
    follow_chance = _get_probability("follow chance")
    return like_chance, follow_chance


def assert_network(network: Optional[SocialNetwork]) -> bool:
    if network is None:
        print("Error: network has not been loaded yet.")
        res = False
    else:
        res = True
    return res


def new_post(person: Person) -> None:
    text = input("Enter post text: ")
    person.make_post(text)


def save_network_serialised(network: SocialNetwork) -> None:
    if assert_network(network):
        path = input("Enter file path: ")
        try:
            with open(path, "wb") as file:
                pickle.dump(network, file)
        except OSError as e:
            print(f"Error writing to file: {e.strerror}")
        # Again, Python docs don't say which exceptions can be raised by pickle.dump().
        except Exception as e:
            print(f"Error serialising network: {e}")


def display_network(network: SocialNetwork) -> None:
    if assert_network(network):
        print("Following:")
        if network.person_count:
            for person in network.people:
                following_str = ", ".join(map(str, person.following))
                print(f"  {person} : {following_str}")
        else:
            print("<no people>")
        print()

        print("Post likes:")
        if network.post_count:
            for post in network.posts:
                likers_str = ", ".join(map(str, post.likers))
                print(f"  {post} : {likers_str}")
        else:
            print("<no posts>")


def network_statistics(network: SocialNetwork) -> None:
    if assert_network(network):
        print("People by popularity:")
        if network.person_count:
            for person in people_by_popularity(network):
                print(f"  {person.follower_count} followers : {person}")
        else:
            print("<no people>")
        print()

        print("Posts by popularity:")
        if network.post_count:
            for post in posts_by_popularity(network):
                print(f"  {post.like_count} likes : {post}")
        else:
            print("<no posts>")


def save_network(network: SocialNetwork) -> None:
    if assert_network(network):
        path = input("Enter file path: ")
        try:
            with open(path, "w") as file:
                for person in network.people:
                    file.write(f"{person.name}\n")
                for person in network.people:
                    for f in person.following:
                        file.write(f"{person.name}:{f.name}\n")
        except OSError as e:
            print(f"Error writing to file: {e}")


def run_timestep(network: SocialNetwork, like_chance: float, follow_chance: float) -> None:
    if assert_network(network):
        if None in (like_chance, follow_chance):
            print("Error: like and follow probabilities are not set.")
        else:
            print("Evaluating timestep...", end="")
            evolve_network(network, like_chance, follow_chance)
            print(" done")


def add_person(network: SocialNetwork) -> None:
    if assert_network(network):
        name = input("Enter new person's name: ")
        if not name or name.isspace():
            print("Error: name cannot be empty or whitespace.")
        else:
            try:
                network.add_person(name)
            except ValueError as e:
                print(f"Error: {e}")


def inspect_person(network: SocialNetwork) -> None:
    if assert_network(network):
        name = input("Enter name of person to view: ")
        try:
            person = network.find_person(name)
        except ValueError:
            print(f"Error: person with name {name} doesn't exist.")
        else:
            selection = None
            while selection is None or selection not in (5, 6):
                print("Operations:")
                print("  1) View statistics")
                print("  2) Make post")
                print("  3) Follow someone")
                print("  4) Unfollow someone")
                print("  5) Delete person")
                print("  6) Exit submenu")
                print()

                selection = None
                while selection is None:
                    selection = input("Enter an option: ")
                    try:
                        selection = int(selection)
                    except ValueError:
                        print("Error: selection must be an integer.")
                        selection = None
                    else:
                        if not 1 <= selection <= 6:
                            print("Error: selection must be >= 1 and <=6.")
                            selection = None

                print()
                if selection == 1:
                    person_statistics(person)
                elif selection == 2:
                    new_post(person)
                elif selection == 3:
                    follow_person(network, person)
                elif selection == 4:
                    unfollow_person(network, person)
                elif selection == 5:
                    network.delete_person(person)
                    del person
                print()


def person_statistics(person: Person) -> None:
    print(f"{person.name}'s statistics:")
    print(f"  Post count: {person.post_count}")
    print(f"  Follower count: {person.follower_count}")
    print(f"  Following count: {person.following_count}")


def follow_person(network: SocialNetwork, person: Person) -> None:
    name = input("Enter name of person to follow: ")
    try:
        person2 = network.find_person(name)
        person.follow(person2)
    except ValueError as e:
        print(f"Error: {e}")


def unfollow_person(network: SocialNetwork, person: Person) -> None:
    name = input("Enter name of person to unfollow: ")
    try:
        person2 = network.find_person(name)
        person.unfollow(person2)
    except ValueError as e:
        print(f"Error: {e}")
