import json
import sys
import random
import math

import my_json_encoder
import my_display
import my_discretisation
import my_end_point
import my_goal_generation
import my_robot


######################################
# Comparer deux generations de goals #
######################################
f = sys.argv[1]

f1 = open("{}_g.json".format(f), "r")
f2 = open("{}_2_g.json".format(f), "r")

goals1 = json.load(fp=f1)
goals2 = json.load(fp=f2)

for g1, g2 in zip(goals1, goals2):
    if g1 != g2:
        print("{} \t {}".format(g1, g2))
    else:
        print("same")

##################################
# Generation direction aleatoire #
##################################
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

#     mag = random.uniform(0,1)
#     pos.append((x*mag, y*mag, z*mag))

# my_display.draw_points_cloud(pos, max_dist = 1)


######################
# Animation du robot #
######################
# poppy = my_robot.Robot()

# my_display.animation(poppy)

#############################################
# Affichage des points / goals d'un fichier #
#############################################
# f = sys.argv[1]
# end_points = []
# goals = []

# the_file = "{}_ep.json".format(f)
# stream = open(the_file, "r")
# string_ep = json.load(fp=stream)
# end_points = my_json_encoder.decode(string_ep)
# stream.close()

# the_file = "{}_g.json".format(f)
# stream = open(the_file, "r")
# goals = json.load(fp=stream)
# stream.close()

# my_display.draw_ep_and_goal(end_points, goals)




#############################################
# Suivre direction d'algo FrontierGenerator #
#############################################
# class false_grid(my_discretisation.Discretisation):
#     def __init__(self):
#         #Recréation du init pour changer le min & max
#         self.min = (-1.5, -1.5, -1.5)
#         self.max = (1.5, 1.5, 1.5)

#         self.precision = [
#             math.floor((ma-mi)/cell_size)+1
#             for mi, ma in zip(_MIN, _MAX)
#         ]

#         Le tableau contenant les données de la discrétisation
#         self.table = [[[0
#             for _ in range(self.precision[2])]
#             for _ in range(self.precision[1])]
#             for _ in range(self.precision[0])]
#         # La taille d'une cellule
#         self.size = cell_size
#         # Garde en mémoire les cellules visitées
#         self.visited = []

#         # Retour au comportement normal pendant l'affichage
#         self.display = False

#     def get_cell(self, pos, override = False):
#         if self.display or override:
#             return super().get_cell(pos)


#         for i in range(3):
#             if pos[i] < 0 or pos[i] >= self.precision[i]:
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

# my_display.draw_points_cloud(points, 1)