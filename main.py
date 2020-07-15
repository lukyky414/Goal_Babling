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
# gg = my_goal_generation.FrontierGenerator(NN = nn)
gg = my_goal_generation.AgnosticGenerator(robot = poppy)

end_points, _ = my_learning.Goal_Babling(robot=poppy, NN = nn, GG = gg)

# table = my_analyse.discretization(end_points, (-1, -1, -1), (1, 1, 1), 20)

# my_display.draw_discretization(table, (-1, -1, -1), (1, 1, 1), 20, 0.0001)

# my_analyse.plot_dist_to_origin(robot=poppy, endpoints=end_points)

# my_analyse.plot_x_y_z_distribution(robot=poppy, endpoints=end_points)

# err = my_analyse.error(robot=poppy, endpoints=end_points)
# print("Distance moyenne entre un goal et le résultat: {}".format(err))

my_display.draw_points_cloud(end_points=end_points, robot=poppy)

# my_display.animation(robot=poppy)

# err = my_nearest_neighbor.test_neirest_neighboor(robot=poppy)

# my_display.animation(robot=poppy)

# angles = my_robot.get_random_posture_angles(robot=poppy)
# posture = my_robot.get_posture(robot=poppy, angles=angles)

# for a in angles:
#     print(a*180/math.pi)

# my_display.display_robot(robot=posture)

# points, _ = my_learning.Goal_Babling(robot=poppy, total_steps=50000)

# my_display.draw_points_cloud(points=points)
