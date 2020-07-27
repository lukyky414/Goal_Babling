import sys

if __name__ != "__main__":
    print("This file needs to be run as main", file=sys.stderr)
    sys.exit(1)

import os.path
import json

import my_robot
import my_nearest_neighbor
import my_goal_generation
import my_option
import my_json_encoder

#Attention, doit etre le meme que DIRECTORY dans main_goals.py
GOAL_DIRECTORY = "files"

DIRECTORY = "files/InverseModel"

#Récupération des options & paramètres
options = my_option.get_options_result()

if options.debug:
    print("Loading config...")

f = options.file

name = f[f.rfind("/")+1:]

if not os.path.isfile("{}.dat".format(f)):
    print("No .dat file found for '{}'.".format(f), file=sys.stderr)
    sys.exit(1)
if not os.path.isfile("{}.idx".format(f)):
    print("No .idx file found for '{}'.".format(f), file=sys.stderr)
    sys.exit(1)


g = "{}/Goals.json".format(GOAL_DIRECTORY)
if not os.path.isfile(g):
    print("File not found '{}'.".format(g), file=sys.stderr)
    sys.exit(1)

#Création du robot
poppy = my_robot.Robot()
nn = None

#save_load=False --> Loading file
nn = my_nearest_neighbor.RtreeNeighbor(save_load=False, f=f)

poppy.set_nn(nn)

#Chargement de la liste de but
f = open(g, "r")
goals = json.load(fp=f)
f.close()

if options.debug:
    print("Generating results...")

res = []
for g in goals:
    posture = poppy.inv_model(g)
    endpoint = poppy.get_end_point(posture)
    res.append(endpoint)

if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)
f = open("{}/{}.json".format(DIRECTORY, name), "w")
json.dump(res, fp=f, cls=my_json_encoder.EP_Encoder)
f.close()

if options.debug:
    print("Done.")