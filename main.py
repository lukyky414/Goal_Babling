import random
import my_display
import my_robot
import my_learning
import math

SEED = 0
random.seed(SEED)

my_poppy = my_robot.Robot()

my_display.animation(robot=my_poppy)


# angles = my_robot.get_random_posture_angles(robot=my_poppy)
# posture = my_robot.get_posture(robot=my_poppy, angles=angles)

# for a in angles:
#     print(a*180/math.pi)

# my_display.display_robot(robot=posture)

# points, _ = my_learning.Goal_Babling(robot=my_poppy, total_steps=50000)

# my_display.draw_points_cloud(points=points)
