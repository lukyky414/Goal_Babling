import my_robot
import random

def generate_goal(robot : my_robot.Robot, coef = 1.4):
    """Genère un but à atteindre pour le `robot`"""

    size_x, size_y, size_z = robot.bounds

    goal = (
        random.uniform(size_x[0] * coef, size_x[1] * coef),
        random.uniform(size_y[0] * coef, size_y[1] * coef),
        random.uniform(size_z[0] * coef, size_z[1] * coef)
    )

    return goal