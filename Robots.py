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

    def __init__(self, size, axe, angle_min=0, angle_max=360, loop=False):
        """`size` is the size of the arm provide in an (X, Y, Z) tuple
        `axe` is the axe around wich the articulation rotate (X, Y & Z coefficient of rotation)
        `angle_min` & `angle_max` are the maximum angle that can be reached
        `loop` define if the motor can execute multiple 360 roation (angle will be consider mod 360)"""

        #Vérification des paramètres
        if len(size) != 3:
            print("Articulation3D.__init__: `size` need 3 coordinate. Got {}".format(len(size)), file=sys.stderr)
            sys.exit(1)
        self.size = size
        if len(axe) != 3:
            print("Articulation3D.__init__: `axe` need 3 coefficient. Got {}".format(len(axe)), file=sys.stderr)
            sys.exit(1)
        elif axe[0] < 0 or axe[0] > 1 or axe[1] < 0 or axe[1] > 1 or axe[2] < 0 or axe[2] > 1:
            print("Articulation3D.__init__: `axe` coefficient wrong. ({},{},{}). Suspected coefficient between 0 and 1.".format(axe[0], axe[1], axe[2]), file=sys.stderr)
            sys.exit(1)
        
        #Attribution des valeurs
        #Normalisation du vecteur axe
        x, y, z = axe
        taille = np.sqrt(x**2 + y**2 + z**2)
        self.axe = (x/taille, y/taille, z/taille)

        self.angle_min = angle_min
        self.angle_max = angle_max
        self.loop = loop

        x, y, z = size
        self.translation = np.array(
            (
                ( 1, 0, 0, x),
                ( 0, 1, 0, y),
                ( 0, 0, 1, z),
                ( 0, 0, 0, 1)
            )
        )
    
    def execute(self, base_pos, angle):
        """Return the position (Rotation Matrix) at the end of the articulation.
        `base_pos` is the position (Rotation Matrix) at the base of the articulation
        `angle` is the angle this articulation will turn (around its `Articulation3D.axe`) within the limit defined."""

        if self.loop:
            angle = angle % 360
        elif angle < self.angle_min:
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

        transformation = rot.dot(self.translation)

        return base_pos.dot(transformation)
        
class Arm3D():
    """A 3D model of a Robotic Arm"""

    def __init__(self, articulations):
        """`articulations` must be type of Articulation3D. Size is not limited."""
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
        self.posture = [(0,0,0)] * (len(articulations)+1)
        self.end_point = (0,0,0)
    
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
        
        self.end_point = (pos[0][3], pos[1][3], pos[2][3])

        return (pos[0][3], pos[1][3], pos[2][3])