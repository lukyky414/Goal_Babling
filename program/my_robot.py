from pypot.creatures import PoppyErgoJr
import random
import math
import sys

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
        self.motor_limit = []
        for m in self.robot.motors:
            mi, ma = m.angle_limit
            if ma < mi:
                t = ma
                ma = mi
                mi = t
            
            self.motor_range.append(ma - mi)
            self.motor_limit.append((mi, ma))
        
    def ik_inv_model(self, goal : tuple):
        g = [[1, 0, 0, goal[0]],
        [0, 1, 0, goal[1]],
        [0, 0, 1, goal[2]],
        [0, 0, 0, 1]]
        #Max iter = 3 -> valeur pour temps de calcul faible
        #Max iter = 1000 -> valeur par defaut pour precision haute
        q = self.robot.chain.inverse_kinematics(g)
        posture = self.robot.chain.convert_from_ik_angles(q)

        return posture
    
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

        for i, limit in zip(range(self.nb_joints), self.motor_limit):
            p = 0
            for ep, c in zip(nears, coefs):
                p += ep.posture[i] * c
            
            if p < limit[0]:
                p = limit[0]
            if p > limit[1]:
                p = limit[1]

            posture.append(p)

        return posture
        
    
    def get_end_point(self, angles : list) -> EndPoint:
        """Retourne le `end_point` du robot en executant les `angles` donnés en degré"""
        res_list = self.get_posture_pos(angles)

        ep = EndPoint(angles, res_list[-1])

        return ep

    def get_posture_pos(self, angles : list) -> list:
        """Retourne la liste des matrices de rotation de chacunes des sections en executant les `angles` donnés en degré"""
        list_angles = self.robot.chain.convert_to_ik_angles(angles)

        res = self.robot.chain.forward_kinematics(joints=list_angles, full_kinematics=True)

        return res
    
    def get_random_angles(self) -> list:
        """Retourne une liste d'angle aléatoire éxecutable par le robot dans les limites de ses moteurs"""
        res = list()
        for limit in self.motor_limit:
            res.append(random.uniform(limit[0], limit[1]))
        return res
    
    def randomize_posture(self, angles : list, perturbation : float) -> list:
        """Modifie aléatoirement la posture donnée par `angles` dans les limites des moteurs du robot"""
        res = list()
        for angle, limit, _range in zip(angles, self.motor_limit, self.motor_range):
            res.append(random.uniform(
                max(limit[0], angle - perturbation * _range),
                min(limit[1], angle + perturbation * _range)
            ))
        
        return res
    
    def get_angle_bounds(self) -> list:
        """Retourne les limites d'angles de chacun des moteurs"""
        return self.motor_limit
    
    def set_nn(self, NN : NearestNeighbor):
        """Permet de changer le NearestNeighbor utilisé pour calculer le modèle inverse."""
        self.nn = NN


if __name__ == "__main__":
    #Permet de faire bouger le robot réel.
    def send_cmd(cmd, topic):
        global socket_simu, socket_real
        socket_simu.publish_on_topic(cmd, topic)

        res = input("Is command valid?")

        if res == "y":
            print("Sending to real robot")
            socket_real.publish_on_topic(cmd, topic)
    
    from py_ergojr.network.messages import Message
    from py_ergojr.network.zmq_publisher import ZmqPublisher
    import time
    import my_nearest_neighbor
    import sys
    import json
    import my_json_encoder
    import gzip

    filename = sys.argv[1]

    with gzip.open("{}".format(filename), "rb") as f:
        ep_str = json.load(fp=f)
        end_points = my_json_encoder.decode(ep_str)

    nn = my_nearest_neighbor.RtreeNeighbor()

    #Taille de barre de chargement
    nb_batch = 10
    #arrondis a l'inferieur
    i_tot = len(end_points)
    batch_size = int( i_tot / nb_batch)
    if batch_size == 0:
        batch_size = 1
    i=0
    for ep in end_points:
        #Affichage de la barre de chargement
        if i%batch_size == 0 or i%1000 == 0:
            print("[", end='')
            for j in range(nb_batch-1):
                if j < i/batch_size:
                    print("#", end='')
                else:
                    print(" ", end='')
            print("] {}/{}".format(i,i_tot), end='\r')
        i=i+1
        #Ajout du point dans la base
        nn.add_end_point(ep)

    poppy = Robot()
    poppy.set_nn(nn)
    
    # socket_real = ZmqPublisher("6666", host="10.0.0.2", bound=False, debug=True)
    socket_simu = ZmqPublisher("6666", host="localhost", bound=False, debug=True)
    # socket_real.start()
    socket_simu.start()


    msg_handler = Message()

    # msg = "m1:off|m2:off|m3:off|m4:off|m5:off|m6:off"
    # send_cmd(msg_handler.make("stiff",msg), "EJTELEOP")

    # msg = "dt:2|m1:0|m2:0|m3:-45|m4:0|m5:-45|m6:0"
    # socket_real.publish_on_topic(msg_handler.make("move",msg,"Q"), "EJTELEOP")
    # send_cmd(msg_handler.make("move",msg,"Q"), "EJTELEOP")

    # input("Enter")


    # for i in range(12):
    #     msg = "m{}:off".format((i-1)%5+2)
    #     msg += "|m{}:blue".format(i%5+2)
    #     msg += "|m{}:white".format((i+1)%5+2)
    #     msg += "|m{}:red".format((i+2)%5+2)
    #     socket_real.publish_on_topic(msg_handler.make("led",msg), "EJTELEOP")
    #     time.sleep(0.5)


    # msg = "dt:2|m1:0|m2:0|m3:0|m4:0|m5:0|m6:0"
    # socket_simu.publish_on_topic(msg_handler.make("move",msg,"Q"), "EJTELEOP")
    # input ("Enter to start")

    # rep = "y"
    # while rep != "n":
    #     posture = poppy.get_random_angles()

    #     msg = "dt:2"
    #     for i in range(6):
    #         msg += "|m{}:{}".format(i+1, posture[i])
        
    #     socket_simu.publish_on_topic(msg_handler.make("move", msg, "Q"), "EJTELEOP")
    #     rep = input(":")


    rep = "r"
    while rep == "r":
        pos = input("Enter 3 coordinates:")
        x, y, z = pos.split(" ")
        x, y, z = float(x), float(y), float(z)

        # x = 0
        # y = 0
        # z = 0.3

        input("Enter pour rest")
        
        msg = "dt:2"
        socket_simu.publish_on_topic(msg_handler.make("rest",msg), "EJTELEOP")

        input("Enter pour ikpy")
        
        posture = poppy.ik_inv_model((x,y,z))
        msg = "dt:2"
        for i in range(6):
            msg += "|m{}:{}".format(i+1, posture[i])

        # send_cmd(msg_handler.make("move", "dt:2|x:{}|y:{}|z:{}".format(x, y, z), "X"), "EJTELEOP")
        socket_simu.publish_on_topic(msg_handler.make("move", msg, "Q"), "EJTELEOP")

        input("Enter pour rest")

        msg = "dt:2"
        socket_simu.publish_on_topic(msg_handler.make("rest",msg), "EJTELEOP")

        input("Enter pour catalogue")

        posture = poppy.inv_model((x,y,z))
        msg = "dt:2"
        for i in range(6):
            msg += "|m{}:{}".format(i+1, posture[i])
        
        socket_simu.publish_on_topic(msg_handler.make("move", msg, "Q"), "EJTELEOP")

        rep = input("Enter r to restart. ")
        # rep = "n"


    # msg = "dance:start"
    # socket_real.publish_on_topic(msg_handler.make("invoke", msg), 'EJPRIM')

    # input("Enter")

    # msg = "dance:stop"
    # socket_real.publish_on_topic(msg_handler.make("invoke", msg), 'EJPRIM')

    # msg = "dt:2|m1:-180|m4:0|m5:35|m6:35|m2:-120|m3:50"
    # socket_real.publish_on_topic(msg_handler.make("move",msg,"Q"), "EJTELEOP")

    # input("Enter")

    # msg = "m1:off|m2:off|m3:off|m4:off|m5:off|m6:off"
    # socket_real.publish_on_topic(msg_handler.make("stiff",msg), "EJTELEOP")
    # msg = "m1:off|m2:off|m3:off|m4:off|m5:off|m6:off"
    # socket_real.publish_on_topic(msg_handler.make("led",msg), "EJTELEOP")

    # socket_real.close()
    socket_simu.close()