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

#Attention, doit etre le meme que DIRECTORY dans main_learning.py
LEARNING_DIRECTORY = "files/NearestNeighbor"
#Attention, doit etre le meme que DIRECTORY dans main_goals.py
GOAL_DIRECTORY = "files"

DIRECTORY = "files/InverseModel"

#Récupération des options & paramètres
options = my_option.get_options_result()

if options.debug:
    print("Loading config")

f = options.file

name = f[f.rfind("/")+1:]
if name[-4:] == ".dat":
    name = name[:-4]
if name[-8:] == "_ep.json":
    name = name[:-8]
if name[-7:] == "_g.json":
    name = name[:-7]

if not os.path.isfile("{}/{}.dat".format(LEARNING_DIRECTORY, name)):
    print("No .dat file found for '{}'.".format(name), file=sys.stderr)
    sys.exit(1)
if not os.path.isfile("{}/{}.idx".format(LEARNING_DIRECTORY, name)):
    print("No .idx file found for '{}'.".format(name), file=sys.stderr)
    sys.exit(1)


g = "{}/Goals.json".format(GOAL_DIRECTORY)
if not os.path.isfile(g):
    print("File not found '{}'.".format(g), file=sys.stderr)
    sys.exit(1)

#Création du robot
poppy = my_robot.Robot()
nn = None

if options.debug:
    print("Loading files")
#save_load=False --> Loading file
nn = my_nearest_neighbor.RtreeNeighbor(save_load=False, f="{}/{}".format(LEARNING_DIRECTORY, name))

poppy.set_nn(nn)

#Chargement de la liste de but
f = open(g, "r")
goals = json.load(fp=f)
f.close()

if options.debug:
    print("Generating results")

if options.debug:
    #Taille de barre de chargement
    nb_batch = 10
    #arrondis a l'inferieur
    batch_size = int((len(goals)) / nb_batch)
    if batch_size == 0:
        batch_size = 1
    i=0
res = []
for g in goals:
    if options.debug:
        i=i+1
        if i%batch_size == 0:
            print("[", end='')
            for j in range(nb_batch-1):
                if j < i/batch_size:
                    print("#", end='')
                else:
                    print(" ", end='')
            print("] {}/{}".format(i,len(goals)), end='\r')
    posture = poppy.inv_model(g)
    endpoint = poppy.get_end_point(posture)
    res.append(endpoint)

if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)
f = open("{}/{}.json".format(DIRECTORY, name), "w")
json.dump(res, fp=f, cls=my_json_encoder.EP_Encoder)
f.close()

if options.debug:
    print("Done.                           ")