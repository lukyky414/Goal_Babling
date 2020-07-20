import random
import my_display
import my_robot
import my_learning
import my_nearest_neighbor
import my_goal_generation
import math
import my_analyse

SEED = 0
random.seed(SEED)

poppy = my_robot.Robot()


nn = my_nearest_neighbor.RtreeNeighbor()
gg = my_goal_generation.FrontierGenerator(p = 0.5, min = (-1, -1, -1), max = (1, 1, 1), precision = (200, 200, 200))

print("Learning Frontier")
my_learning.Goal_Babling(robot=poppy, NN = nn, GG = gg)

grid = gg.grid

my_display.draw_discretization(grid = grid)

# nn2 = my_nearest_neighbor.RtreeNeighbor()
# gg2 = my_goal_generation.AgnosticGenerator(robot = poppy)

# print("Learning Agnostic")
# my_learning.Goal_Babling(robot=poppy, NN = nn, GG = gg)

# grid2 = gg2.grid


# diff1 = my_analyse.difference_discretisation(grid1=grid, grid2=grid2)

# diff2 = my_analyse.difference_discretisation(grid1=grid2, grid2=grid)




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
