from pypot.creatures import PoppyErgoJr
import random
from math import pi

def get_pos_from_matrix(matrix = None, matrixes = None):
    if matrix != None:
        return (matrix[0][3], matrix[1][3], matrix[2][3])
    
    if matrixes != None:
        res = list()
        for matrix in matrixes:
            res.append((matrix[0][3], matrix[1][3], matrix[2][3]))
        return res
    
    return None

class Robot():

    def __init__(self):
        self.robot = PoppyErgoJr(simulator="poppy-simu")
        print("Open the simulator here:")
        print("  http://simu.poppy-project.org/poppy-ergo-jr/")
    
    def get_position(self, angles : list):
        """Retourne la matrice de rotation du `end_point` en executant les `angles` donnés en degré"""
        list_angles = list()
        list_angles.append(0)
        for a in angles:
            list_angles.append(a/180*pi)
        list_angles.append(0)

        return self.robot.chain.forward_kinematics(joints=list_angles, full_kinematics=False)

    def get_posture(self, angles : list):
        """Retourne la liste des matrices de rotation de chacunes des sections en executant les `angles` donnés en degré"""
        list_angles = list()
        list_angles.append(0)
        for a in angles:
            list_angles.append(a/180*pi)
        list_angles.append(0)

        return self.robot.chain.forward_kinematics(joints=list_angles, full_kinematics=True)
    
    def get_random_angles(self):
        """Retourne une liste d'angle aléatoire éxecutable par le robot dans les limites de ses moteurs"""
        res = list()
        for motor in self.robot.motors:
            res.append(random.uniform(motor.angle_limit[0], motor.angle_limit[1]))
        return res
    
    def randomize_posture(self, angles : list):
        """Modifie aléatoirement la posture donnée par `angles` dans les limites des moteurs du robot"""
        # déformation
        d = 0.01

        res = list()
        for motor, angle in zip(self.robot.motors, angles):
            res.append(random.uniform(
                max(motor.angle_limit[0], angle - d),
                min(motor.angle_limit[1], angle + d)
            ))
        
        return res
    
    def get_bounds(self):
        """Retourne les limites d'angles de chacun des moteurs"""
        res = list()
        for motor in self.robot.motors:
            res.append(motor.angle_limit)
        return res
    
    def get_joint_number(self):
        """Retourne le nombre de section du robot. Utile pour initialiser une liste d'angle."""
        return len(self.robot.motors)

    def get_size(self):
        """Retourne la taille du robot. Si c'est un bras robotique, donner la somme de la longueur de chacune des sections."""

        return self.robot.chain._length