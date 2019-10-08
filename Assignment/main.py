from network import SocialNetwork
from simulation import evolve_network

import random


network = SocialNetwork()

for i in range(100):
    network.add_person(str(i))


for person1 in network.people:
    for person2 in network.people:
        if person1 != person2:
            if random.random() < 0.05:
                try:
                    person1.follow(person2)
                except ValueError:
                    pass


for i in range(60):
    print(f"Timestep {i+1}")
    for person in network.people:
        if random.random() < 0.1:
            person.make_post(f"{person} in timestep {i+1}.")
    evolve_network(network, 0.05, 0.1)


pass


print("Followers:")
for person in network.people:
    print(f"\t{person}: {person.following_count}")
