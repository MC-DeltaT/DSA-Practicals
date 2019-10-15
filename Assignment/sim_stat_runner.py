from common import unique_file
from network_generator import random_network

import os
import subprocess


PEOPLE_MIN = 10
PEOPLE_MAX = 100
PEOPLE_STEP = 10

# Integer percentages only.
LIKE_CHANCE_MIN = 20
LIKE_CHANCE_MAX = 100
LIKE_CHANCE_STEP = 20

# Integer percentages only.
FOLLOW_CHANCE_MIN = 20
FOLLOW_CHANCE_MAX = 100
FOLLOW_CHANCE_STEP = 20


for person_count in range(PEOPLE_MIN, PEOPLE_MAX + PEOPLE_STEP, PEOPLE_STEP):
    for like_chance in range(LIKE_CHANCE_MIN, LIKE_CHANCE_MAX + LIKE_CHANCE_STEP, LIKE_CHANCE_STEP):
        like_chance /= 100
        for follow_chance in range(FOLLOW_CHANCE_MIN, FOLLOW_CHANCE_MAX + FOLLOW_CHANCE_STEP, FOLLOW_CHANCE_STEP):
            follow_chance /= 100
            print(f"~~~~~~~~~  people={person_count} like_chance={like_chance} follow_chance={follow_chance} ~~~~~~~~~")
            netfile_path = None
            eventfile_path = None
            try:
                network, events = random_network(person_count, 5, 4, 2, 2.5)

                with unique_file("netfile", ".txt") as netfile:
                    netfile_path = netfile.name
                    netfile.write(network)

                with unique_file("eventfile", ".txt") as eventfile:
                    eventfile_path = eventfile.name
                    eventfile.write(events)

                subprocess.run(f"python SocialSim.py -s {netfile_path} {eventfile_path} {like_chance} {follow_chance}")
            except Exception as e:
                print(f"Error: {repr(e)}")
            finally:
                if netfile_path is not None:
                    try:
                        os.remove(netfile_path)
                    except OSError: pass
                if eventfile_path is not None:
                    try:
                        os.remove(eventfile_path)
                    except OSError: pass
