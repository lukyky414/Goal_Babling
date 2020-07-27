import sys

if __name__ != "__main__":
    print("This file needs to be run as main", file=sys.stderr)
    sys.exit(1)

import random
import os
import json

from my_robot import Robot
from my_goal_generation import FrontierGenerator
from my_option import get_options_goal

DIRECTORY = "files"

options = get_options_goal()
if options.debug:
    print("Generating goals...")

poppy = Robot()

#Les points générés seront tous les memes
random.seed(options.seed)

goals = []
for _ in range(1000):
    dir = FrontierGenerator.get_random_dir()
    dist = random.uniform(0, poppy.size)
    goals.append([p*dist for p in dir])


if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)
f = open("{}/Goals.json".format(DIRECTORY), "w")
json.dump(goals, fp=f)
f.close()

if options.debug:
    print("Done.")
