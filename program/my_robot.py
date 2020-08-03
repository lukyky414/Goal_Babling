from pypot.creatures import PoppyErgoJr
import random
import math

from my_end_point import EndPoint
from my_nearest_neighbor import NearestNeighbor, dist

#Le robot est basé sur PoppyErgoJr qui est une Pypot.Creature

class Robot():

    def __init__(self):
        self.robot = PoppyErgoJr(simulator="poppy-simu")
        # print("Open the simulator here:")
        # print("  http://simu.poppy-project.org/poppy-ergo-jr/")
        self.nn = None
        self.nb_joints = len(self.robot.motors)
        self.size = 0

        #On ingore la taille de la base qui est à 1, mais on somme le reste des links
        for link in self.robot.chain.links[1:]:
            self.size += link.length
        
        self.motor_range = []
        for m in self.robot.motors:
            mi, ma = m.angle_limit
            if ma < mi:
                t = ma
                ma = mi
                mi = t
            
            self.motor_range.append(ma - mi)
    
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

        for i in range(self.nb_joints):
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
            list_angles.append(a/180*math.pi)
        list_angles.append(0)

        res = EndPoint(angles, self.robot.chain.forward_kinematics(joints=list_angles, full_kinematics=False))

        return res

    def get_posture_pos(self, angles : list) -> list:
        """Retourne la liste des matrices de rotation de chacunes des sections en executant les `angles` donnés en degré"""
        list_angles = list()
        list_angles.append(0)
        for a in angles:
            list_angles.append(a/180*math.pi)
        list_angles.append(0)

        res = self.robot.chain.forward_kinematics(joints=list_angles, full_kinematics=True)

        return res
    
    def get_random_angles(self) -> list:
        """Retourne une liste d'angle aléatoire éxecutable par le robot dans les limites de ses moteurs"""
        res = list()
        for motor in self.robot.motors:
            res.append(random.uniform(motor.angle_limit[0], motor.angle_limit[1]))
        return res
    
    def randomize_posture(self, angles : list, perturbation : float) -> list:
        """Modifie aléatoirement la posture donnée par `angles` dans les limites des moteurs du robot"""
        res = list()
        for angle, motor, _range in zip(angles, self.robot.motors, self.motor_range):
            res.append(random.uniform(
                max(motor.angle_limit[0], angle - perturbation * _range),
                min(motor.angle_limit[1], angle + perturbation * _range)
            ))
        
        return res
    
    def get_angle_bounds(self) -> list:
        """Retourne les limites d'angles de chacun des moteurs"""
        res = list()
        for motor in self.robot.motors:
            res.append(motor.angle_limit)
        return res
    
    def set_nn(self, NN : NearestNeighbor):
        """Permet de changer le NearestNeighbor utilisé pour calculer le modèle inverse."""
        self.nn = NN


# if __name__ == "__main__":


    # #Permet de faire bouger le robot réel.
    
    # from py_ergojr.network.messages import Message
    # from py_ergojr.network.zmq_publisher import ZmqPublisher
    # import time
    # from my_nearest_neighbor import RtreeNeighbor
    # import sys

    # poppy = Robot()

    # nn = RtreeNeighbor(false, f=sys.argv[1])
    
    # socket_real = ZmqPublisher("6666", host="poppy", bound=False, debug=True)
    # socket_simu = ZmqPublisher("6666", host="localhost", bound=False, debug=True)
    # socket_real.start()
    # socket_simu.start()

    # def send_cmd(cmd, topic):
    #     socket_simu.pusblish_on_topic(cmd, topic)

    #     res = input("Is command valid?")

    #     if res == y:
    #         socket_real.publish_on_topic(cmd, topic)

    # msg_handler = Message()

    # # msg = "m1:off|m2:off|m3:off|m4:off|m5:off|m6:off"
    # #  send_cmd(msg_handler.make("stiff",msg), "EJTELEOP")

    # # msg = "dt:2|m1:0|m2:0|m3:-45|m4:0|m5:-45|m6:0"
    # #  send_cmd(msg_handler.make("move",msg,"Q"), "EJTELEOP")

    # # input("Enter")


    # for i in range(12):
    #     msg = "m{}:off".format((i-1)%5+2)
    #     msg += "|m{}:blue".format(i%5+2)
    #     msg += "|m{}:white".format((i+1)%5+2)
    #     msg += "|m{}:red".format((i+2)%5+2)
    #     send_cmd(msg_handler.make("led",msg), "EJTELEOP")
    #     time.sleep(0.5)

    # # msg = "dance:start"
    # #  send_cmd(msg_handler.make("invoke", msg), 'EJPRIM')

    # # input("Enter")

    # # msg = "dance:stop"
    # #  send_cmd(msg_handler.make("invoke", msg), 'EJPRIM')


    # input("Enter")

    # # msg = "dt:2|m1:-180|m4:0|m5:35|m6:35|m2:-120|m3:50"
    # #  send_cmd(msg_handler.make("move",msg,"Q"), "EJTELEOP")
    # # time.sleep(2)

    # msg = "m1:off|m2:off|m3:off|m4:off|m5:off|m6:off"
    #  send_cmd(msg_handler.make("stiff",msg), "EJTELEOP")
    # msg = "m1:off|m2:off|m3:off|m4:off|m5:off|m6:off"
    #  send_cmd(msg_handler.make("led",msg), "EJTELEOP")

    # socket.close()