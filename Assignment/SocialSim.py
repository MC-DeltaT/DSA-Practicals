import interactive_mode
import simulation_mode

import sys


def print_usage() -> None:
    print("Usage:")
    print("\t Interactive mode: python3 SocialSim.py -i")
    print("\t Simulation mode: python3 SocialSim.py -s <netfile> <eventfile> <like_prob> <follow_prob>")


if len(sys.argv) == 2 and sys.argv[1] == "-i":
    interactive_mode.main()
elif len(sys.argv) == 6 and sys.argv[1] == "-s":
    simulation_mode.main()
else:
    print_usage()
