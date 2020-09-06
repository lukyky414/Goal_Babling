import json
import sys
import random
import scipy
import math
import gzip
import shutil
import numpy

from py_ergojr.network.messages import Message
from py_ergojr.network.zmq_publisher import ZmqPublisher

from my_files_paths import *
import my_json_encoder
import my_display
import my_discretisation
import my_end_point
import my_goal_generation
import my_robot
import my_nearest_neighbor


###########################
# Perturbation de posture #
###########################
# poppy = my_robot.Robot()

# my_display._background_color = (255, 255, 255)
# my_display._cloud_point_color = (0, 0, 0)
# my_display._sphere_color = (0, 0, 0, 0.1)

# posture = (0, 0, 0, 0, 0, 0)
# ep = poppy.get_end_point(posture)

# end_points = [ep]
# i = 0
# for i in range(500):
#     print(i, end="\r")
#     p = poppy.randomize_posture(posture, 0.05)
#     ep = poppy.get_end_point(p)

#     end_points.append(ep)
# print()

# my_display.draw_points_cloud(end_points, robot=poppy)

###############################
# Exemple Poppy Motor Babling #
###############################
# poppy = my_robot.Robot()
# posture = poppy.get_random_angles()
# representation = poppy.get_posture_pos(posture)

# my_display._background_color = (255, 255, 255)
# my_display._section_color = (0, .3, 0, 1)
# my_display._joint_color = (0, .3, 0, 1)
# my_display._draw_fps_bool = False

# my_display.display_robot(representation)


####################################
# Test Modèle Inverse sur le Robot #
####################################
# poppy = my_robot.Robot()
# socket_simu = ZmqPublisher("6666", host="localhost", bound=False, debug=True)
# socket_simu.start()
# msg_handler = Message()

# while True:
#     pos = input("Enter 3 coordinates:")
#     x, y, z = pos.split(" ")

#     goal = (float(x), float(y), float(z))
#     g = numpy.eye(4)
#     g[:3,3] = goal
#     q = poppy.robot.chain.inverse_kinematics(g)

#     print(q)
#     posture = poppy.robot.chain.convert_from_ik_angles(q)
#     print(q)

#     msg = "dt:2"
#     for i in range(6):
#         msg += "|m{}:{}".format(i+1, posture[i])
    
#     socket_simu.publish_on_topic(msg_handler.make("move", msg, "Q"), "EJTELEOP")


#     ep = poppy.get_end_point(posture)
#     r = ep.matrix
#     p = ep.get_pos()
#     a = ep.posture

#     print(a)
#     print()

#     print(g)
#     print()
#     for l in r:
#         for x in l:
#             if x < 0.01:
#                 print("0                 \t", end="")
#             elif x == 1:
#                 print("1                 \t", end="")
#             else:
#                 print(x, end="\t")
#         print()
#     print()
#     for x in p:
#         if x < 0.01:
#             print("0                 \t", end="")
#         elif x == 1:
#             print("1                 \t", end="")
#         else:
#             print(x, end="\t")
#     print()
#     print()
#     print()
#     print()
#     print()
#     print()
#     print()
#     print()
#     print()

#########################
# Comparer Goal et Ikpy #
#########################
# gofp = "{}/{}".format(MAIN_DIR, GOAL_FILE)
# ikfp = "{}/{}".format(MAIN_DIR, IKPY_FILE)

# gof = open(gofp, "r")
# ikf = open(ikfp, "r")

# goals = json.load(fp=gof)
# gof.close()

# iks = json.load(fp=ikf)
# ikpys = my_json_encoder.decode(iks)
# ikf.close()

# my_display.draw_ep_and_goal(ikpys, goals)


############################################
# Vérification du volume de la convex hull #
############################################
# points = []
# for _ in range(100000):
#     points.append(my_goal_generation.FrontierGenerator.get_random_dir())

# print(4 * math.pi / 3)
# print(scipy.spatial.ConvexHull(points=points).volume)

#######################################################
# Comparer la sphere robot et la liste des end_points #
#######################################################
# poppy = my_robot.Robot()

# my_display._background_color = (255, 255, 255)
# my_display._cloud_point_color = (0, 0, 0)
# my_display._sphere_color = (0, 0, 0, 0.1)

# end_points = []
# i = 0
# for i in range(8000):
#     print(i, end="\r")
#     p = poppy.get_random_angles()
#     ep = poppy.get_end_point(p)

#     end_points.append(ep)
# print()

# my_display.draw_points_cloud(end_points, sphere=poppy.size)

############################
# Generation but aleatoire #
############################
# poppy = my_robot.Robot()
# pos = []

# angle = 2*math.pi - (math.pi/2)
# rot = 3*math.pi/4

# for _ in range(10000):
#     u = random.uniform(0,1)
#     v = random.uniform(0,1)

#     theta = angle*u + rot
#     phi = math.acos(2*v-1)

#     x = math.cos(theta) * math.sin(phi)
#     y = math.sin(theta) * math.sin(phi)
#     z = abs(math.cos(phi))

#     mag = random.uniform(0,poppy.size)
#     mag = math.pow(random.uniform(0,1), 1/3) * poppy.size
#     # mag = poppy.size
#     # if z < 0.1:
#     pos.append((x*mag, y*mag, z*mag))

# my_display._background_color = (255, 255, 255)
# my_display._section_color = (0, .3, 0, 1)
# my_display._joint_color = (0, .3, 0, 1)
# my_display._cloud_point_color = (0, 0, 0)
# # my_display.draw_points_cloud(pos, robot=poppy)
# my_display.draw_points_cloud(pos)

######################
# Animation du robot #
######################
# poppy = my_robot.Robot()

# my_display.animation(poppy)

#############################################
# Suivre direction d'algo FrontierGenerator #
#############################################
# my_discretisation._MIN = -1
# my_discretisation._MAX = 1
# class false_grid(my_discretisation.Discretisation):
#     def __init__(self):
#         super().__init__(10, True)
#         self.display = False

#     def get_cell(self, pos):
#         if self.display:
#             return super().get_cell(pos)

#         for i in range(3):
#             if pos[i] < 0 or pos[i] >= self.nb_divs :
#                 return 0

#         if super().get_cell(pos)==0:
#             self.visited.append(pos)
#             self.add_to_pos(pos)

#             return 1

# ep = my_end_point.EndPoint(
#     [],
#     (
#         (0, 0, 0, 0.003),
#         (0, 0, 0, 0.003),
#         (0, 0, 0, 0.003),
#         (0, 0, 0, 0)
#     )
# )

# grid = false_grid()
# gg = my_goal_generation.FrontierGenerator(1, grid)
# gg.init([ep])
# d = gg.newGoal()

# grid.display = True
# my_display.draw_discretization(grid, 0.2, d)


###############################
# Distribution des directions #
###############################
# points = []
# for _ in range(10000):
#     points.append(my_goal_generation.FrontierGenerator.get_random_dir())

# my_display._cloud_point_color = (1, 0, 0)
# my_display.draw_points_cloud(points)