import random
import my_display
import my_robot
import my_learning
from ikpy.chain import Chain
import math

SEED = 0
random.seed(SEED)

my_ikpy = Chain.from_urdf_file("./poppy_from_ikpy.urdf")
my_poppy = Chain.from_urdf_file("./poppy_from_poppy-ergo-jr.urdf")

my_display.animation(robot=my_poppy)


# angles = my_robot.get_random_posture_angles(robot=my_poppy)
# posture = my_robot.get_posture(robot=my_poppy, angles=angles)

# for a in angles:
#     print(a*180/math.pi)

# my_display.display_robot(robot=posture)

# points, _ = my_learning.Motor_Babling(robot=my_poppy)

# my_display.draw_points_cloud(points=points)
