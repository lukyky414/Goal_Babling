from pypot.creatures import PoppyErgoJr
import random
from math import pi, sqrt

from my_end_point import EndPoint
from my_nearest_neighbor import NearestNeighbor, dist

import sys

class Robot():

    def __init__(self):
        self.robot = PoppyErgoJr(simulator="poppy-simu")
        # print("Open the simulator here:")
        # print("  http://simu.poppy-project.org/poppy-ergo-jr/")
        self.nn = None
        self.nb_joints = len(self.robot.motors)
    
    def inv_model(self, goal : tuple):
        """Le modèle inverse du robot. Retourne une liste d'angle pour atteindre le point demandé."""
        if self.nn is None:
            raise "Robots have no Nearest Neighbor. Inv_Model is impossible."

        nears = self.nn.nearest_list(goal, 3)

        dists = []
        tot = 0
        for ep in nears:
            d = dist(ep.get_pos(), goal)
            tot += d
            dists.append(d)
        coefs = []
        for d in dists:
            coefs.append(d/tot)

        posture = []

        for i in range(self.nb_joint)
            p = 0
            for ep, c in zip(nears, coefs):
                p += ep.posture[i] * c
            
            if p > self.robot.motors[i].angle_limit[1]:
                p = self.robot.motors[i].angle_limit[1]
            if p < self.robot.motors[i].angle_limit[0]:
                p = self.robot.motors[i].angle_limit[0]
            posture.append(p)

        return posture
        
    
    def get_end_point(self, angles : list) -> EndPoint:
        """Retourne le `end_point` du robot en executant les `angles` donnés en degré"""
        list_angles = list()
        list_angles.append(0)
        for a in angles:
            list_angles.append(a/180*pi)
        list_angles.append(0)

        res = EndPoint(angles, self.robot.chain.forward_kinematics(joints=list_angles, full_kinematics=False))

        return res

    def get_posture(self, angles : list) -> list:
        """Retourne la liste des matrices de rotation de chacunes des sections en executant les `angles` donnés en degré"""
        list_angles = list()
        list_angles.append(0)
        for a in angles:
            list_angles.append(a/180*pi)
        list_angles.append(0)

        res = self.robot.chain.forward_kinematics(joints=list_angles, full_kinematics=True)

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

    def get_size(self):
        """Retourne la distance entre la base et l'endpoint rencontré le plus éloigné de la base."""
        return self.furthest
    
    def reset(self):
        """Permet de réinitialiser les données sauvegardées après un apprentissage (comme le point le plus loin ou les limites)"""
        self.bounds = None
        self.furthest = 0
    
    def set_nn(self, NN : NearestNeighbor):
        """Permet de changer le NearestNeighbor utilisé pour calculer le modèle inverse."""
        self.nn = NN