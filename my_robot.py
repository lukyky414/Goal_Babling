"""Fichier contenant les differentes classes de robots."""

import math
import random
import numpy as np

class Robot:
    """Classe representant un bras robotique en 3d."""
    # Liste des positions des sections [ (axe_x, axe_y, axe_z), (axe_x, axe_y, axe_z), ... ]
    posture = [(0, 0, 0)]
    # Position du point final du robot (axe_x, axe_y, axe_z)
    end_point = (0, 0, 0)
    # Nombre d'articulations du robot
    dim = 0

    def random_angles(self):
        """Retourne une liste d'angle aleatoire et uniforme dans les limites predefinies par le robot."""
        raise NotImplementedError()

    def execute(self, angles):
        """Retourne la position du point final du robot.
        `angles` - Liste d'angle, en degree et dans les limites predefinies, de taille `Robot.dim`, qu'executera le robot."""
        raise NotImplementedError()

class Robot2d(Robot):
    """Classe representant un bras robotique en 2d.
    Herite de `my_robot.Robot` avec une des calculs simples pour la 2d."""
    _limit = 0

    def __init__(self, dim, limit=150):
        """`dim` - Nombre de section du robot.
        `limit` - Angle maximum d'une section en degree [-limit, limit]. Default `150`"""
        self.dim = dim
        self._limit = limit
        self.execute(angles=[0]*self.dim)

    def random_angles(self):
        return [random.uniform(-self._limit, self._limit) for _ in range(self.dim)]

    def execute(self, angles):
        curr_x, curr_y = 0, 0

        # Commencer les angles a 90 pour que le bras a angle 0 soit dirige vers le haut
        sum_a = math.pi / 2

        # Longueur d'une section
        length = 1.0 / self.dim

        # Reinitialisation de la posture
        self.posture = [(0, 0, 0)]

        for angle in angles:
            if angle > self._limit:
                angle = self._limit
            elif angle < -self._limit:
                angle = -self._limit

            sum_a = sum_a + angle * math.pi / 180

            curr_x = curr_x + math.cos(sum_a) * length
            curr_y = curr_y + math.sin(sum_a) * length

            self.posture.append(curr_x, curr_y, 0)

        self.end_point = (curr_x, curr_y, 0)

        return self.end_point

class Robot3d(Robot):
    """Classe representant un bras robotique en 3d compose d'articulations.
    Herite de `my_robot.Robot` avec une des calculs pour la 3d."""

    def __init__(self, articulations):
        """`articulations` est la liste d'articulations de type `my_robot.Articulation` du robot."""

        self._articulations = articulations
        self.dim = len(articulations)

        self.execute(angles=[0]*self.dim)

    def random_angles(self):
        return [random.uniform(a.angle_min, a.angle_max) for a in self._articulations]

    def execute(self, angles):

        pos = np.array(
            (
                (1, 0, 0, 0),
                (0, 1, 0, 0),
                (0, 0, 1, 0),
                (0, 0, 0, 1)
            )
        )

        self.posture = [(0, 0, 0)]

        for i in range(self.dim):
            section = self._articulations[i]
            angle = angles[i]

            pos = section.execute(base_pos=pos, angle=angle)
            self.posture.append((pos[0][3], pos[1][3], pos[2][3]))

        self.end_point = (pos[0][3], pos[1][3], pos[2][3])

        return self.end_point

class Articulation():
    """Classe representant une section d'un Robot3d.
    Permet de separer les calculs"""
    _limit = (0, 0)
    _matrix = np.array((
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0)
    ))

    def __init__(self, origin, axe, limit):
        """`origin` est la position et rotation de la section, en ( (axe_x, axe_y, axe_z), (r, p, axe_y) ). r, p & axe_y en radians.
        `axe` est le vecteur autour duquel la section effectuera la rotation.
        `limit` est un couple avec l'angle minimum et l'angle maximum executable par l'articulation (min, max) en degree"""

        #Normalisation du vecteur axe
        axe_x, axe_y, axe_z = axe
        taille = np.sqrt(axe_x**2 + axe_y**2 + axe_z**2)
        self.axe = (axe_x/taille, axe_y/taille, axe_z/taille)

        self._limit = limit

        # Differente matric pour executer les rotation autour des axes x, y et z pour r(raw), p(pitch) et y(yaw) respectivement.
        rot_x = np.array(
            (
                (1, 0, 0, 0),
                (0, math.cos(origin[1][0]), -math.sin(origin[1][0]), 0),
                (0, math.sin(origin[1][0]), math.cos(origin[1][0]), 0),
                (0, 0, 0, 1)
            )
        )
        rot_y = np.array(
            (
                (math.cos(origin[1][1]), 0, math.sin(origin[1][1]), 0),
                (0, 1, 0, 0),
                (-math.sin(origin[1][1]), 0, math.cos(origin[1][1]), 0),
                (0, 0, 0, 1)
            )
        )
        rot_z = np.array(
            (
                (math.cos(origin[1][2]), -math.sin(origin[1][2]), 0, 0),
                (math.sin(origin[1][2]), math.cos(origin[1][2]), 0, 0),
                (0, 0, 1, 0),
                (0, 0, 0, 1)
            )
        )

        pos_x, pos_y, pos_z = origin[0]

        translation = np.array(
            (
                (1, 0, 0, pos_x),
                (0, 1, 0, pos_y),
                (0, 0, 1, pos_z),
                (0, 0, 0, 1)
            )
        )

        # Matrice de transformation de cette articulation.
        self._matrix = translation.dot(rot_x).dot(rot_y).dot(rot_z)


    def execute(self, base_pos, angle):
        """Retourn la position de la fin de l'articulation en matrice de rotation.
        `base_pos` est la position en matrice de rotation de la base de l'articulation.
        `angle` est l'angle execute par cette articulation dans les limites predefinies."""

        if angle < self._limit[0]:
            angle = self._limit[0]
        elif angle > self._limit[1]:
            angle = self._limit[1]

        angle = angle * math.pi / 180

        cos, sin = math.cos(angle), math.sin(angle)
        _cos = 1-cos

        axe_x, axe_y, axe_z = self.axe

        #Attention, utiliser Fennec sous android. Firefox, chrome & autres ne montrent aucunes parenthèses dans les formules.
        # https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/glRotate.xml
        rot = np.array(
            (
                (axe_x*axe_x*_cos+cos,       axe_x*axe_y*_cos-axe_z*sin, axe_x*axe_z*_cos+axe_y*sin, 0),
                (axe_y*axe_x*_cos+axe_z*sin, axe_y*axe_y*_cos+cos,       axe_y*axe_z*_cos-axe_x*sin, 0),
                (axe_x*axe_z*_cos-axe_y*sin, axe_y*axe_z*_cos+axe_x*sin, axe_z*axe_z*_cos+cos,       0),
                (0, 0, 0, 1)
            )
        )

        return base_pos.dot(self._matrix).dot(rot)
