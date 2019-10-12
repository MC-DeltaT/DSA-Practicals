from network import SocialNetwork
from simulation import evolve_network

import random


people = 100
post_chance = 0.1
timesteps = 50


network = SocialNetwork(people, round(timesteps * people * post_chance))

for i in range(people):
    network.add_person(str(i))


for person1 in network.people:
    for person2 in network.people:
        if person1 != person2:
            if random.random() < 0.05:
                try:
                    person1.follow(person2)
                except ValueError:
                    pass

print("Following count:")
for person in network.people:
    print(f"\t{person}: {person.following_count}")

for i in range(timesteps):
    print(f"Timestep {i+1}")
    for person in network.people:
        if random.random() < post_chance:
            person.make_post(f"{person} in timestep {i+1}.")
    evolve_network(network, 0.05, 0.1)


pass


print("Following count:")
for person in network.people:
    print(f"\t{person}: {person.following_count}")
