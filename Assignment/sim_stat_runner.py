from network_generator import generate_network

import subprocess


PEOPLE_MIN = 50
PEOPLE_MAX = 300
PEOPLE_STEP = 50

# Integer percentages only.
LIKE_CHANCE_MIN = 10
LIKE_CHANCE_MAX = 100
LIKE_CHANCE_STEP = 10

# Integer percentages only.
FOLLOW_CHANCE_MIN = 10
FOLLOW_CHANCE_MAX = 100
FOLLOW_CHANCE_STEP = 10


for person_count in range(PEOPLE_MIN, PEOPLE_MAX + PEOPLE_STEP, PEOPLE_STEP):
    for like_chance in range(LIKE_CHANCE_MIN, LIKE_CHANCE_MAX + LIKE_CHANCE_STEP, LIKE_CHANCE_STEP):
        like_chance /= 100
        for follow_chance in range(FOLLOW_CHANCE_MIN, FOLLOW_CHANCE_MAX + FOLLOW_CHANCE_STEP, FOLLOW_CHANCE_STEP):
            follow_chance /= 100
            print(f"~~~~~~~~~  people={person_count} like_chance={like_chance} follow_chance={follow_chance} ~~~~~~~~~")
            try:
                generate_network(person_count, 5, 4, 2, 2.5)
                subprocess.run(f"python SocialSim.py -s netfile_random.txt eventfile_random.txt {like_chance} {follow_chance}")
            except Exception as e:
                print(e)
