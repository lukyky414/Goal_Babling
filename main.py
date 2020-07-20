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
gg = my_goal_generation.FrontierGenerator(p = 0.5, min = (-1, -1, -1), max = (1, 1, 1), precision = (50, 50, 50))


print("Learning Frontier")
start = time()
end_points, goals = my_learning.Goal_Babling(robot=poppy, NN = nn, GG = gg, motor_babling_steps=5000, total_steps=7000)
stop = time()
print("{}ms".format(math.floor((stop - start) * 1000)))
print()

grid = gg.grid


nn2 = my_nearest_neighbor.RtreeNeighbor()
gg2 = my_goal_generation.AgnosticGenerator(robot = poppy)

print("Learning Agnostic")
start = time()
end_points2, goals2 = my_learning.Goal_Babling(robot=poppy, NN = nn2, GG = gg2, motor_babling_steps=5000, total_steps=7000)
stop = time()
print("{}ms".format(math.floor((stop - start) * 1000)))
print()

grid2 = my_discretisation.Discretisation(min = (-1, -1, -1), max = (1, 1, 1), precision = (50, 50, 50))
for ep in end_points2:
    grid2.add_point(ep)


my_display.draw_diff(grid, grid2)


# my_analyse.plot_dist_to_origin(robot=poppy, endpoints=end_points)

# my_analyse.plot_x_y_z_distribution(robot=poppy, endpoints=end_points)

# err = my_analyse.error(
# print("Distance moyenne entre un goal et le résultat: {}".format(err))

# my_display.draw_points_cloud(end_points=end_points)

# my_display.animation(robot=poppy)

# err = my_nearest_neighbor.test_neirest_neighboor(robot=poppy)

# my_display.animation(robot=poppy)

# angles = my_robot.get_random_posture_angles(robot=poppy)
# posture = my_robot.get_posture(robot=poppy, angles=angles)

# for a in angles:
#     print(a*180/math.pi)

# my_display.display_robot(robot=posture)

# points, _ = my_learning.Goal_Babling(robot=poppy, total_steps=50000)
