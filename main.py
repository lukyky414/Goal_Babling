"""Fichier principal d'utilisation de my_display, my_robot et my_learning."""

import random
import my_robot
import my_display
import my_learning

SEED = 0
random.seed(SEED)

POPPY = my_robot.Robot3d(articulations=[
    my_robot.Articulation(
        origin=(
            (0, 0, 0.0327993216120967),
            (-6.12303176911189e-17, 0, 0)
        ),
        axe=(0, -1, 0),
        limit=(-150, 150)
    ),
    my_robot.Articulation(
        origin=(
            (0, 0, 0.0240006783879033),
            (1.5707963267949, 0, 0)
        ),
        axe=(-1, 0, 0),
        limit=(-90, 125)
    ),
    my_robot.Articulation(
        origin=(
            (0, 0.054, 0),
            (0, 0, 0)
        ),
        axe=(-1, 0, 0),
        limit=(-90, 90)
    ),
    my_robot.Articulation(
        origin=(
            (0, 0.0298217741221248, 0),
            (3.141592653589, 0, 0)
        ),
        axe=(0, 0, 1),
        limit=(-150, 150)
    ),
    my_robot.Articulation(
        origin=(
            (0, -0.0151782258778753, -0.048),
            (-1.5707963267949, 0, 0)
        ),
        axe=(-1, 0, 0),
        limit=(-90, 90)
    ),
    my_robot.Articulation(
        origin=(
            (0, 0.054, 0),
            (1.5707963267949, 1.5707963267949, 0)
        ),
        axe=(0, 0, -1),
        limit=(-110, 90)
    )
])

def main_func():
    """Fonction principale pour eviter les erreurs pylint"""
    pos, _ = my_learning.Motor_Babling(POPPY, steps=10000)

    my_display.draw_points_cloud(points=pos)

if __name__ == "__main__":
    main_func()
