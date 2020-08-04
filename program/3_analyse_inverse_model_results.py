import sys

if __name__ != "__main__":
    print("This file needs to be run as main", file=sys.stderr)
    sys.exit(1)

import os.path
import json
import math
import numpy

from my_files_paths import *
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

RESULTS = {}

#Récupération des options & paramètres
options = my_option.get_options_analyse()

if options.debug:
    print("Step 3: Analyse results of using the Inverse Model")
    print("Loading Config")


f = options.file

name = f[f.rfind("/")+1:]
#Ignorer le .json si présent
if name[-5:] == ".json":
    name = name[:-5]

IS_IKPY = "ikpy" in name
    
if not os.path.isfile("{}/{}/{}.json".format(MAIN_DIR, RES_DIR, name)):
    print("No Inverse Model Results '.json' file found for '{}'.".format(name), file=sys.stderr)
    sys.exit(1)

g = "{}/{}".format(MAIN_DIR, GOAL_FILE)
if not os.path.isfile(g):
    print("File not found '{}'.".format(g), file=sys.stderr)
    sys.exit(1)


if not IS_IKPY and not os.path.isfile("{}/{}/{}_ep.json".format(MAIN_DIR, INV_DIR, name)):
    print("No End Point List '_ep.json' file found for '{}'.".format(name), file=sys.stderr)
    sys.exit(1)

poppy = Robot()

if options.debug:
    print("Loading files", end="")

#Chargement de la liste des end_points atteint avec le modèle inverse
f = open("{}/{}/{}.json".format(MAIN_DIR, RES_DIR, name), "r")
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

if not IS_IKPY:
    #Chargement des end_points dans la base du modèle inverse
    f = open("{}/{}/{}_ep.json".format(MAIN_DIR, INV_DIR, name), "r")
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
_distances = []
#Somme des distances et distances au carré
for ep, g in zip(end_points_im, goals):
    pos = ep.get_pos()
    d = dist(g, pos)
    _distances.append(d)

distances = numpy.array(_distances)
# distances.sort()
# RESULTS["distances"] = distances.to_array()

if options.debug:
    print("Calculating volume")

if IS_IKPY:
    vol = 0
else:
    grid = Discretisation(options.nb_div, save_visited=False)
    for ep in end_points:
        grid.add_point(ep)
    vol = grid.nb_visited * (grid.size ** 3)

if options.debug:
    print("Generating results")

# RESULTS["vol"] = vol

theorical_vol = (poppy.size ** 3) * math.pi * 4/3
RESULTS["rvo"] = vol / theorical_vol
# RESULTS["tvo"] = theorical_vol


RESULTS["min"] = distances.min()

RESULTS["1qa"] = numpy.quantile(distances, 0.25)

RESULTS["moy"] = distances.mean()

RESULTS["med"] = numpy.median(distances)

RESULTS["3qa"] = numpy.quantile(distances, 0.75)

RESULTS["max"] = distances.max()

RESULTS["var"] = distances.var()
##########
#Output des résultats
##########

if options.debug:
    print("Output in files")

if not os.path.exists("{}/{}".format(MAIN_DIR, ANL_DIR)):
    os.makedirs("{}/{}".format(MAIN_DIR, ANL_DIR))

f = open("{}/{}/{}.json".format(MAIN_DIR, ANL_DIR, name), "w")
json.dump(RESULTS, fp=f)
f.close()

if options.debug:
    print("Done.")
