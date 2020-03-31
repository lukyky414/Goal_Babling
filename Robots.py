import sys
from math import pi, cos, sin
import random
import numpy as np
from OpenGL.GL import glRotatef, glMatrixMode, glLoadMatrixf, glGetFloatv, GL_MODELVIEW, GL_MODELVIEW_MATRIX

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

    def random_angle(self):
        return [random.uniform(-self.limit, self.limit) for _ in range(self.dim)]

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
            if a < -self.limit :
                print("Arm2D.execute: angle is out of bound. min:{} < angle:{}. Reducing to {}".format(-self.limit, a, -self.limit), file=sys.stderr)
                a = -self.limit
            elif a > self.limit:
                print("Arm2D.execute: angle is out of bound. angle:{} < max:{}. Reducing to {}".format(self.limit, a, self.limit), file=sys.stderr)
                a = self.limit

            sum_a += np.radians(a)
            x += np.cos(sum_a)*length
            y += np.sin(sum_a)*length

            self.posture.append((x, y))

        self.end_point = (x,y)

        return x, y

class Articulation3D():

    def __init__(self, origin, axe, angle_min=0, angle_max=360):
        """`origin` is the position and the rotation of this articulation provided in an ( (x, y, z), (r, p, y)). rpy in rad
        `axe` is the vector around wich the articulation rotate
        `angle_min` & `angle_max` are the maximum angle that can be reached in °"""

        #Normalisation du vecteur axe
        x, y, z = axe
        taille = np.sqrt(x**2 + y**2 + z**2)
        self.axe = (x/taille, y/taille, z/taille)

        self.angle_min = angle_min
        self.angle_max = angle_max

        #deduction de la matrice de rotation de cette partie
        pos_x, pos_y, pos_z = origin[0]

        rot_x = np.array(
            (
                (1, 0, 0, 0),
                (0, cos(origin[1][0]), -sin(origin[1][0]), 0),
                (0, sin(origin[1][0]), cos(origin[1][0]), 0),
                (0, 0, 0, 1)
            )
        )
        rot_y = np.array(
            (
                (cos(origin[1][1]), 0, sin(origin[1][1]), 0),
                (0, 1, 0, 0),
                (-sin(origin[1][1]), 0, cos(origin[1][1]), 0),
                (0, 0, 0, 1)
            )
        )
        rot_z = np.array(
            (
                (cos(origin[1][2]), -sin(origin[1][2]), 0, 0),
                (sin(origin[1][2]), cos(origin[1][2]), 0, 0),
                (0, 0, 1, 0),
                (0, 0, 0, 1)
            )
        )

        translation = np.array(
            (
                (1, 0, 0, pos_x),
                (0, 1, 0, pos_y),
                (0, 0, 1, pos_z),
                (0, 0, 0, 1)
            )
        )

        self.matrix = translation.dot(rot_x).dot(rot_y).dot(rot_z)


    def execute(self, base_pos, angle):
        """Return the position (Rotation Matrix) at the end of the articulation.
        `base_pos` is the position (Rotation Matrix) at the base of the articulation
        `angle` is the angle this articulation will turn (around its `Articulation3D.axe`) within the limit defined."""

        if angle < self.angle_min:
            print("Articulation3D.execute: angle is out of bound. min:{} < angle:{}".format(self.angle_min, angle), file=sys.stderr)
            angle = self.angle_min
        elif angle > self.angle_max:
            print("Articulation3D.execute: angle is out of bound. angle:{} < max:{}".format(angle, self.angle_max), file=sys.stderr)
            angle = self.angle_max

        angle = np.radians(angle)

        c, s = np.cos(angle), np.sin(angle)
        _c = 1-c

        x, y, z = self.axe

        #Attention, utiliser Fennec sous android. Firefox, chrome & autres ne montrent aucunes parenthèses dans les formules.
        # https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/glRotate.xml
        rot = np.array(
            (
                (x*x*_c+c, x*y*_c-z*s, x*z*_c+y*s, 0),
                (y*x*_c+z*s, y*y*_c+c, y*z*_c-x*s, 0),
                (x*z*_c-y*s, y*z*_c+x*s, z*z*_c+c, 0),
                (0, 0, 0, 1)
            )
        )

        return base_pos.dot(self.matrix).dot(rot)

class Arm3D():
    """A 3D model of a Robotic Arm"""

    def __init__(self, articulations, end_joint=(0, 0, 0)):
        """`articulations` must be type of Articulation3D. Size is not limited.
        `end_joint` is the final vector after the last Articulation for the calculation of the end_point."""

        if len(articulations) <= 0:
            print("Arm3D.__init__: The robot must have at least one articulation.", file=sys.stderr)
            sys.exit(1)
        if type(articulations[0]) != Articulation3D:
            print("Arm3D.__init__: `articulations` must be a list of Articulation3D", file=sys.stderr)
            sys.exit(1)

        self.articulations = articulations
        self.base_pos = np.array(
            (
                (1, 0, 0, 0),
                (0, 1, 0, 0),
                (0, 0, 1, 0),
                (0, 0, 0, 1)
            )
        )
        self.posture = [(0, 0, 0)] * (len(articulations)+1)
        self.end_point = (0, 0, 0)
        self.dim = len(articulations)
        self.end_joint = np.array(
            (
                (1, 0, 0, end_joint[0]),
                (0, 1, 0, end_joint[1]),
                (0, 0, 1, end_joint[2]),
                (0, 0, 0, 1)
            )
        )

    def random_angle(self):
        return [random.uniform(a.angle_min, a.angle_max) for a in self.articulations]

    def execute(self, angle):
        """Return the position of the end of the arm.
        `angle` is an array of the same size of `Arm3D.articulations`"""

        if len(angle) != len(self.articulations):
            print("Arm3D.execute: len(angles) ({}) does not match len(Arm3D.articulations) ({})".format(len(angles), len(self.articulations)), file=sys.stderr)
            sys.exit(1)

        pos = self.base_pos

        self.posture = [(0, 0, 0)]

        for section, angle in zip(self.articulations, angle):
            pos = section.execute(base_pos=pos, angle=angle)
            self.posture.append((pos[0][3], pos[1][3], pos[2][3]))

        pos = pos.dot(self.end_joint)
        self.posture.append((pos[0][3], pos[1][3], pos[2][3]))

        self.end_point = (pos[0][3], pos[1][3], pos[2][3])

        return (pos[0][3], pos[1][3], pos[2][3])
