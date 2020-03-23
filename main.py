import random
from Robots import Arm3D, Articulation3D
from display import draw_one_3d_robot

SEED = 0
random.seed(SEED)

if __name__ == "__main__":
    poppy_robot = Arm3D(articulations=[
        Articulation3D(
            size=(0, 0.2, 0),
            axe=(0, 1, 0),
            loop=True
        ),
        Articulation3D(
            size=(0, 0.2, 0),
            axe=(1, 0, 0),
            angle_min=-130,
            angle_max=130
        ),
        Articulation3D(
            size=(0, 0.2, 0),
            axe=(1, 0, 0),
            angle_min=-130,
            angle_max=130
        ),
        Articulation3D(
            size=(0, 0, 0.2),
            axe=(0, 1, 0),
            loop=True
        ),
        Articulation3D(
            size=(0, 0, 0.2),
            axe=(1, 0, 0),
            angle_min=-130,
            angle_max=130
        ),
        Articulation3D(
            size=(0, 0, 0.2),
            axe=(1, 0, 0),
            angle_min=-130,
            angle_max=130
        )
    ])

    poppy_robot.execute([
        -120,
        130,
        -45,
        180,
        45,
        45
    ])

    draw_one_3d_robot(robot=poppy_robot)
