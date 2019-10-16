from common import unique_file
from network_generator import random_network

import os
import subprocess


PEOPLE_MIN = 225
PEOPLE_MAX = 225
PEOPLE_STEP = 50

# Integer percentages only.
LIKE_CHANCE_START = 100
LIKE_CHANCE_STOP = 10
LIKE_CHANCE_STEP = -10

# Integer percentages only.
FOLLOW_CHANCE_START = 100
FOLLOW_CHANCE_STOP = 10
FOLLOW_CHANCE_STEP = -10


for person_count in range(PEOPLE_MIN, PEOPLE_MAX + PEOPLE_STEP, PEOPLE_STEP):
    like_chance_percent = LIKE_CHANCE_START
    while min(LIKE_CHANCE_START, LIKE_CHANCE_STOP) <= like_chance_percent <= max(LIKE_CHANCE_START, LIKE_CHANCE_STOP):
        like_chance = like_chance_percent / 100
        follow_chance_percent = FOLLOW_CHANCE_START
        while min(FOLLOW_CHANCE_START, FOLLOW_CHANCE_STOP) <= follow_chance_percent <= max(FOLLOW_CHANCE_START, FOLLOW_CHANCE_STOP):
            follow_chance = follow_chance_percent / 100
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

            follow_chance_percent += FOLLOW_CHANCE_STEP
        like_chance_percent += LIKE_CHANCE_STEP
