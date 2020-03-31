import random
from Display import *
from Learning import Motor_Babling
import poppy_ergo_jr

SEED = 0
random.seed(SEED)

if __name__ == "__main__":
    poppy_robot = poppy_ergo_jr.get_robot()

    draw_one_3d_robot(poppy_robot)

    points, angles = Motor_Babling(poppy_robot, steps=50000)

    # draw_multiple_3d_robot(poppy_robot, angles)
    draw_cloud(points)
