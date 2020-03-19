import random
from Robots import Arm2D
from display import motor_babling

SEED = 0
random.seed(SEED)

if __name__ == "__main__":
    arm = Arm2D(dim=100)

    motor_babling(robot=arm)
