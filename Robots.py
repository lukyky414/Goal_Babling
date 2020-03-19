import sys
import numpy as np

class Arm2D():
    """A simple 2d Robotic Arm"""

    def __init__(self, dim=2, limit=150):
        """`dim` is the number of joint in the arm
        `limit` is the max angle possible at each dim (-limit, limit)"""
        self.dim = dim
        self.limit = limit
        #Position de base du robot
        self.posture = [(0.0, 0.0)] * (dim+1)
        self.end_point = (0.0, 0.0)

    def execute(self, angles):
        """Return the position of the end of the arm.
        `angle` is an array of size `Arm2D.dim`"""

        if len(angles) != self.dim:
            print("Arm2D.execute: len(angles) ({}) does not match Arm2D.dim ({})".format(len(angles), self.dim), file=sys.stderr)
            sys.exit(1)

        # Position actuelle
        x, y = 0, 0
        # Somme des angles
        # Un joint à un angle de 0 est dans la direction des dims d'avant
        sum_a = 0
        # Longueur entre deux dims
        length = 1.0 / self.dim
        # Reset la posture actuelle (le 1e dim est forcément à 0,0)
        self.posture = [(x, y)]

        for a in angles:
            sum_a += a / 180 * np.pi
            x += np.cos(sum_a)*length
            y += np.sin(sum_a)*length

            self.posture.append((x, y))

        self.end_point = (x,y)

        return x, y
