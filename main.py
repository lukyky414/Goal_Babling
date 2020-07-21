import random
import my_display
import my_robot
import my_learning
import my_nearest_neighbor
import my_goal_generation
import my_discretisation
import math
import my_analyse
from time import time
import sys


#Le SEED de random change à l'utilisation de pypot.creature
poppy = my_robot.Robot()

SEED = 0
random.seed(SEED)

nn = my_nearest_neighbor.RtreeNeighbor()
grid = my_discretisation.grid()
gg = my_goal_generation.FrontierGenerator(p=0.5, grid=grid)


print("Learning Frontier")
start = time()
end_points, goals = my_learning.Goal_Babling(robot=poppy, NN = nn, GG = gg, motor_babling_steps=2000, total_steps=4000)
stop = time()
print("Computing time: {}ms".format(math.floor((stop - start) * 1000)))
print()

my_analyse.plots_distribution(robot=poppy, endpoints=end_points, precision=200)
