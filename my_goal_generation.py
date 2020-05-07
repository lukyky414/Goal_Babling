import my_robot

def generate_goal(robot : my_robot.Robot):
    """Genère un but à atteindre pour le `robot`"""

    size = robot.get_size()

    goal = (
        random.uniform(-size, size),
        random.uniform(-size, size),
        random.uniform(-size, size)
    )

    return goal