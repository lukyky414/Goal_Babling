from pypot.creatures import PoppyErgoJr
import random
from math import pi, sqrt

from my_end_point import EndPoint

class Robot():

    def __init__(self):
        self.robot = PoppyErgoJr(simulator="poppy-simu")
        # print("Open the simulator here:")
        # print("  http://simu.poppy-project.org/poppy-ergo-jr/")
        # Limites (min, max) des positions rencontrées en (x, y, z) du robot.
        self.bounds = None
        self.furthest = 0

    def __update_end__(self, ep : EndPoint):
        pos = ep.get_pos()
        if self.bounds is None:
            self.bounds = [[pos[0], pos[0]], [pos[1], pos[1]], [pos[2], pos[2]]]
        else:
            for i in range(3):
                if pos[i] < self.bounds[i][0]:
                    self.bounds[i][0] = pos[i]
                if pos[i] > self.bounds[i][1]:
                    self.bounds[i][1] = pos[i]
        
        dist = 0
        for p in pos:
            dist += p**2
        dist = sqrt(dist)

        if dist > self.furthest:
            self.furthest = dist
        
    
    def get_end_point(self, angles : list) -> EndPoint:
        """Retourne le `end_point` du robot en executant les `angles` donnés en degré"""
        list_angles = list()
        list_angles.append(0)
        for a in angles:
            list_angles.append(a/180*pi)
        list_angles.append(0)

        res = EndPoint(angles, self.robot.chain.forward_kinematics(joints=list_angles, full_kinematics=False))

        self.__update_end__(res)

        return res

    def get_posture(self, angles : list) -> list:
        """Retourne la liste des matrices de rotation de chacunes des sections en executant les `angles` donnés en degré"""
        list_angles = list()
        list_angles.append(0)
        for a in angles:
            list_angles.append(a/180*pi)
        list_angles.append(0)

        res = self.robot.chain.forward_kinematics(joints=list_angles, full_kinematics=True)

        ep = EndPoint(angles, res[-1])

        self.__update_end__(ep)

        return res
    
    def get_random_angles(self) -> list:
        """Retourne une liste d'angle aléatoire éxecutable par le robot dans les limites de ses moteurs"""
        res = list()
        for motor in self.robot.motors:
            res.append(random.uniform(motor.angle_limit[0], motor.angle_limit[1]))
        return res
    
    def randomize_posture(self, angles : list) -> list:
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
    
    def get_angle_bounds(self) -> list:
        """Retourne les limites d'angles de chacun des moteurs"""
        res = list()
        for motor in self.robot.motors:
            res.append(motor.angle_limit)
        return res
    
    def get_joint_number(self) -> int:
        """Retourne le nombre de section du robot. Utile pour initialiser une liste d'angle."""
        return len(self.robot.motors)

    def get_size(self):
        """Retourne la distance entre la base et l'endpoint rencontré le plus éloigné de la base."""
        return self.furthest