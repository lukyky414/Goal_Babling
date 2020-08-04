import numpy
import os
import json

from my_files_paths import *
import my_robot
import my_option
import my_json_encoder


poppy = my_robot.Robot()

def inv_mod(goal):
    global poppy
    g = numpy.eye(4)
    g[:3,3] = goal
    #Max iter = 3 -> default value
    q = poppy.robot.chain.inverse_kinematics(g, max_iter=3)
    posture = poppy.robot.chain.convert_from_ik_angles(q)

    return poppy.get_end_point(posture)


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
        i=i+1
        if i%batch_size == 0 or i%1000 == 0:
            print("[", end='')
            for j in range(nb_batch-1):
                if j < i/batch_size:
                    print("#", end='')
                else:
                    print(" ", end='')
            print("] {}/{}".format(i,len(goals)), end='\r')
    #Execution du modele inverse
    endpoint = inv_mod(g)
    res.append(endpoint)


if options.debug:
    print()
    print("Output in file")

if not os.path.exists("{}/{}".format(MAIN_DIR, RES_DIR)):
    os.makedirs("{}/{}".format(MAIN_DIR, RES_DIR))

f = open("{}/{}/ikpy_{}.json".format(MAIN_DIR, RES_DIR, options.n), "w")
json.dump(res, fp=f, cls=my_json_encoder.EP_Encoder)
f.close()

if options.debug:
    print("Done.")