import sys

if __name__ != "__main__":
    print("This file needs to be run as main", file=sys.stderr)
    sys.exit(1)

import os.path
import json
import math

import my_option
import my_json_encoder

from my_nearest_neighbor import dist
from my_discretisation import Discretisation
from my_robot import Robot
from my_nearest_neighbor import RtreeNeighbor
from my_display import draw_discretization

##########
#Chargement des options, début du programme
##########

#Attention, doit etre le meme que DIRECTORY dans main_learning.py
LEARNING_DIRECTORY = "files/NearestNeighbor"
#Attention, doit etre le meme que DIRECTORY dans main_learning.py
INV_MOD_DIRECTORY = "files/InverseModel"

#Attention, doit etre le meme que DIRECTORY dans main_goals.py
GOAL_DIRECTORY = "files"

DIRECTORY = "files/AnalysisResult"
RESULTS = {}

#Récupération des options & paramètres
options = my_option.get_options_analyse()

if options.debug:
    print("Loading Config")


f = options.file

name = f[f.rfind("/")+1:]
#Ignorer le .json si présent
if name[-5:] == ".json":
    name = name[:-5]
    
if not os.path.isfile("{}/{}.json".format(INV_MOD_DIRECTORY, name)):
    print("No Inverse Model .json file found for '{}'.".format(name), file=sys.stderr)
    sys.exit(1)

g = "{}/Goals.json".format(GOAL_DIRECTORY)
if not os.path.isfile(g):
    print("File not found '{}'.".format(g), file=sys.stderr)
    sys.exit(1)


if not os.path.isfile("{}/{}_ep.json".format(LEARNING_DIRECTORY, name)):
    print("No _ep.json file found for'{}'.".format(name), file=sys.stderr)
    sys.exit(1)

poppy = Robot()

if options.debug:
    print("Loading files", end="")

#Chargement de la liste des end_points atteint
f = open("{}/{}.json".format(INV_MOD_DIRECTORY, name), "r")
str_ep_im = json.load(fp=f)
end_points_im = my_json_encoder.decode(str_ep_im)
f.close()

if options.debug:
    print(".", end="")

#Chargement de la liste des but que le modele inverse a essayé d'atteindre
f = open(g, "r")
goals = json.load(fp=f)
f.close()

if options.debug:
    print(".", end="")

#Chargement des end_points dans la base
f = open("{}/{}_ep.json".format(LEARNING_DIRECTORY, name), "r")
str_ep = json.load(fp=f)
end_points = my_json_encoder.decode(str_ep)
f.close()

if options.debug:
    print(".")

##########
#Analyse des résultats
##########

if options.debug:
    print("Getting distances from goals")
#Calcul des distances des points par rapport aux but
distances = []
#Somme des distances et distances au carré
s = 0
s2 = 0
for ep, g in zip(end_points_im, goals):
    pos = ep.get_pos()
    d = dist(g, pos)
    distances.append(d)
    s += d
    s2 += d**2

# RESULTS["distances"] = distances

if options.debug:
    print("Calculating volume")
grid = Discretisation(options.nb_div, save_visited=False)
for ep in end_points:
    grid.add_point(ep)

vol = grid.nb_visited * (grid.size ** 3)
RESULTS["volume"] = vol

theorical_vol = (poppy.size ** 3) * math.pi * 4/3
RESULTS["relative_volume"] = vol / theorical_vol
# RESULTS["theorical_vol"] = theorical_vol

if options.debug:
    print("Calculating other value")
n = len(distances)

m = s / n
RESULTS["moyenne"] = m

v = (s2 - 2*m*s)/n + m**2
RESULTS["variance"] = v

ec = math.sqrt(v)
RESULTS["ecart_type"] = ec


##########
#Output des résultats
##########

if options.debug:
    print("Output in files")

if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)
f = open("{}/{}.json".format(DIRECTORY, name), "w")
json.dump(RESULTS, fp=f)
f.close()


if options.debug:
    print("Done.")
