import sys

if __name__ != "__main__":
    print("This file needs to be run as main", file=sys.stderr)
    sys.exit(1)

import random
import os
import math
import json

from my_files_paths import *
from my_robot import Robot
from my_option import get_options_goal


options = get_options_goal()
if options.debug:
    print("Generating goals")

#Création du robot pour avoir sa taille
poppy = Robot()

random.seed(options.seed)

goals = []

#angle à générer aléatoirement pour avoir le camembert
angle = 2*math.pi - (math.pi/2)
#angle pour faire tourner le camembert
rot = 3*math.pi/4

for _ in range(1000):
    u = random.uniform(0,1)
    v = random.uniform(0,1)

    theta = angle*u + rot
    phi = math.acos(2*v-1)

    x = math.cos(theta) * math.sin(phi)
    y = math.sin(theta) * math.sin(phi)
    z = abs(math.cos(phi))

    dist = math.pow(random.uniform(0,1), 1/3) * poppy.size
    goals.append((x*dist, y*dist, z*dist))


if options.debug:
    print("Output in file")

filename = "{}/{}".format(MAIN_DIR, GOAL_FILE)

f = open(filename, "w")
json.dump(goals, fp=f)
f.close()

if options.debug:
    print("Done.")
