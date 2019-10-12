from network import evolve_network, SocialNetwork
from simulation_mode import simulation_complete

import random


people = 10
post_chance = 0.5


network = SocialNetwork(people, round(people * post_chance))

for i in range(people):
    network.add_person(str(i))


for person1 in network.people:
    for person2 in network.people:
        if person1 != person2:
            if random.random() < 2 / people:
                try:
                    person1.follow(person2)
                except ValueError:
                    pass
    if random.random() < post_chance:
        person1.make_post(f"{person1}: hello.")

print("Following count:")
for person in network.people:
    print(f"\t{person}: {person.following_count}")

i = 1
while not simulation_complete(network):
    print(f"Timestep {i}")
    evolve_network(network, 1, 1)
    i += 1


print("Following count:")
for person in network.people:
    print(f"\t{person}: {person.following_count}")
