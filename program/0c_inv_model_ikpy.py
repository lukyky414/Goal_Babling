import numpy
import os
import json

from my_files_paths import *
import my_robot
import my_option
import my_json_encoder
import my_nearest_neighbor


poppy = my_robot.Robot()

#Récupération des options & paramètres
options = my_option.get_options_ikpy()

if options.debug:
    print("Use IKPY Inverse Model")
    print("Loading config")

g = "{}/{}".format(MAIN_DIR, GOAL_FILE)
if not os.path.isfile(g):
    print("File not found '{}'.".format(g), file=sys.stderr)
    sys.exit(1)


if options.debug:
    print("Loading files")

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
    #Affichage de la barre de chargement
    if options.debug:
        print("[", end='')
        for j in range(nb_batch-1):
            if j < i/batch_size:
                print("#", end='')
            else:
                print(" ", end='')
        print("] {}/{}".format(i,len(goals)), end='\r')
        i=i+1
    #Execution du modele inverse
    endpoint = poppy.get_end_point(poppy.ik_inv_model(g))
    res.append(endpoint)


if options.debug:
    print()
    print("Output in file")


f = open("{}/{}".format(MAIN_DIR, IKPY_FILE), "w")
json.dump(res, fp=f, cls=my_json_encoder.EP_Encoder)
f.close()

if options.debug:
    print("Done.")