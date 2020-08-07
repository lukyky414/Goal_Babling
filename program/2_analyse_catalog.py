import sys

if __name__ != "__main__":
    print("This file needs to be run as main", file=sys.stderr)
    sys.exit(1)

import os.path
import json
import numpy
import math
import scipy

from my_files_paths import *
import my_robot
import my_nearest_neighbor
import my_goal_generation
import my_option
import my_json_encoder
import my_discretisation

#Récupération des options & paramètres
options = my_option.get_options_analyse()

if options.debug:
    print("Step2: Analyse the Inverse Model")
    print("Loading config", end="", flush=True)

#Récupération du nom de fichier
f = options.file

#Seul le nom est utile, on ignore les dossiers et extensions
name = f[f.rfind("/")+1:]
if name[-4:] == ".dat":
    name = name[:-4]
elif name[-4:] == ".idx":
    name = name[:-4]
elif name[-8:] == "_ep.json":
    name = name[:-8]
elif name[-7:] == "_g.json":
    name = name[:-7]

if options.debug:
    print(".", end="", flush=True)

#Vérifier l'existence des fichiers nécessaires
if not os.path.isfile("{}/{}/{}.dat".format(MAIN_DIR, CTL_DIR, name)):
    print("No .dat file found for '{}'.".format(name), file=sys.stderr)
    sys.exit(1)
if not os.path.isfile("{}/{}/{}.idx".format(MAIN_DIR, CTL_DIR, name)):
    print("No .idx file found for '{}'.".format(name), file=sys.stderr)
    sys.exit(1)
if not os.path.isfile("{}/{}/{}_ep.json".format(MAIN_DIR, CTL_DIR, name)):
    print("No _ep.json file found for '{}'.".format(name), file=sys.stderr)
    sys.exit(1)

gl = "{}/{}".format(MAIN_DIR, GOAL_FILE)
if not os.path.isfile(gl):
    print("File not found '{}'.".format(gl), file=sys.stderr)
    sys.exit(1)

ik = "{}/{}".format(MAIN_DIR, IKPY_FILE)
if not os.path.isfile(ik):
    print("File not found '{}'.".format(ik), file=sys.stderr)
    sys.exit(1)

if options.debug:
    print(".")

#Création du robot
poppy = my_robot.Robot()

if options.debug:
    print("Loading files", end="", flush=True)

nn = my_nearest_neighbor.RtreeNeighbor(f="{}/{}/{}".format(MAIN_DIR, CTL_DIR, name))

poppy.set_nn(nn)

#Chargement de la liste des observations du catalogue
f = open("{}/{}/{}_ep.json".format(MAIN_DIR, CTL_DIR, name), "r")
ep_str = json.load(fp=f)
end_points = my_json_encoder.decode(ep_str)
f.close()

if options.debug:
    print(".", end="", flush=True)

#Chargement de la liste de but
f = open(gl, "r")
goals = json.load(fp=f)
f.close()

if options.debug:
    print(".", end="", flush=True)

#Chargement de la liste des observations ikpy
f = open(ik, "r")
ep_str = json.load(fp=f)
ikpys = my_json_encoder.decode(ep_str)
f.close()

if options.debug:
    print(".")

#Calcul des distances aux buts
if options.debug:
    print("Reaching goals", end="", flush=True)

    #Taille de barre de chargement
    nb_batch = 10
    #arrondis a l'inferieur
    i_tot = len(goals)
    batch_size = int( i_tot / nb_batch)
    if batch_size == 0:
        batch_size = 1
    i=0

res_gl = []
res_ik = []
dis_gl = []
dis_ik = []
if options.debug:
    print(".")
for gl, ik in zip(goals, ikpys):
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
            print("] {}/{}".format(i,i_tot), end='\r')
    #Execution du modele inverse
    posture = poppy.inv_model(gl)
    endpoint = poppy.get_end_point(posture)
    d = my_nearest_neighbor.dist(gl, endpoint.get_pos())

    res_gl.append(endpoint)
    dis_gl.append(d)

    #Execution du modele inverse
    posture = poppy.inv_model(ik.get_pos())
    endpoint = poppy.get_end_point(posture)
    d = my_nearest_neighbor.dist(ik.get_pos(), endpoint.get_pos())

    res_ik.append(endpoint)
    dis_ik.append(d)

if options.debug:
    print("Analysing results          ")

distances_gl = numpy.array(dis_gl)
distances_ik = numpy.array(dis_ik)

if options.debug:
    print("Calculating space filling")

    #Taille de barre de chargement
    nb_batch = 10
    #arrondis a l'inferieur
    i_tot = len(end_points)
    batch_size = int( i_tot / nb_batch)
    if batch_size == 0:
        batch_size = 1
    i=0

grid = my_discretisation.Discretisation(options.nb_div, save_visited=False)
for ep in end_points:
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
            print("] {}/{}".format(i,i_tot), end='\r')
    grid.add_point(ep)
remplissage = grid.nb_visited

if options.debug:
    print("Generating results                   ")

#Volume reel
sphere_volume = (poppy.size ** 3) * 4 * math.pi / 3
#Arrondis en nombre de cellule
sphere_volume = math.floor((1 / grid.size**3) * sphere_volume)

#remplissages
print(grid.nb_visited / sphere_volume, end=" ")

#volume
pts = numpy.array([ep.get_pos() for ep in end_points])
print(scipy.spatial.ConvexHull(points=pts).volume, end=" ")

for array in [distances_gl, distances_ik]:
    #moyenne
    print(array.mean(), end=" ")

    #variance
    print(array.var(), end=" ")

    #quartiles
    mi, q1, me, q3, ma = numpy.quantile(array, [0, 0.25, 0.5, 0.75, 1])
    print("{} {} {} {} {}".format(mi, q1, me, q3, ma), end=" ")

print()