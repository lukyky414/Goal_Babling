import sys

if __name__ != "__main__":
    print("This file needs to be run as main")
    sys.exit(1)

import random
import math
from time import time

import my_display
import my_robot
import my_learning
import my_nearest_neighbor
import my_goal_generation
import my_discretisation
import my_analyse
import my_option

# #Le robot étudié est le Poppy
# poppy = my_robot.Robot()

# #Le SEED de random change à l'utilisation de pypot.creature. Réinitialisation nécessaire pour re-création des résultats
# SEED = 0
# random.seed(SEED)

# #Le meilleure Nearest Neighbor utilisé
# nn = my_nearest_neighbor.RtreeNeighbor()

options = my_option.get_options()

print(options)
