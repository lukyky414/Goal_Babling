import sys

if __name__ != "__main__":
    print("This file needs to be run as main", file=sys.stderr)
    sys.exit(1)

import os.path
import json
import numpy
import math
import scipy
import gzip
import shutil
from rtree.core import RTreeError
import Tools
from importlib import reload

from my_files_paths import *
import my_robot
import my_nearest_neighbor
import my_goal_generation
import my_option
import my_json_encoder
import my_discretisation
import my_name_generator

#Récupération des options & paramètres
options = my_option.get_options_analyse()


###########################
# Chargement de la config #
###########################


if options.debug:
    print("Step2: Analyse the Inverse Model")
    print("Loading config")

#Récupération du nom de fichier
f = options.file

#Seul le nom est utile, on ignore les dossiers et extensions
name = f[f.rfind("/")+1:]
if name[-8:] == ".json.gz":
    name = name[:-8]

#Ignorer le numéro d'execution
if name[name.rfind("_")+1:].isnumeric():
    name = name[:name.rfind("_")]
#Pour la completion avec tab, le numero n'est pas forcement mis
if name[name.rfind("_")+1:] == "":
    name = name[:name.rfind("_")]

#Création du robot
poppy = my_robot.Robot()

#Creation de la grille pour le calcul du remplissage
grid = my_discretisation.Discretisation(options.nb_div, save_visited=False)

#Volume reel de la sphere theoriquement atteignable
sphere_volume = (poppy.size ** 3) * 4 * math.pi / 3
#Arrondis en nombre de cellule
sphere_volume = math.floor((1 / grid.size**3) * sphere_volume)

#fichier des but
gl_file = "{}/{}".format(MAIN_DIR, GOAL_FILE)
if not os.path.isfile(gl_file):
    print("File not found '{}'.".format(gl_file), file=sys.stderr)
    sys.exit(1)

#fichier des ikpy(but)
ik_file = "{}/{}".format(MAIN_DIR, IKPY_FILE)
if not os.path.isfile(ik_file):
    print("File not found '{}'.".format(ik_file), file=sys.stderr)
    sys.exit(1)

file_options = my_name_generator.get_options(name)
directory = "{}/{}/".format(MAIN_DIR, CTL_DIR)
if file_options["mb"] == 1:
    directory += "motor_babling"
else:
    directory += file_options["gg"]


###########################
# Chargement des fichiers #
###########################


if options.debug:
    print("Loading files", end="", flush=True)

#Chargement de la liste de but
f = open(gl_file, "r")
goals = json.load(fp=f)
f.close()

if options.debug:
    print(".", end="", flush=True)

#Chargement de la liste des observations ikpy
f = open(ik_file, "r")
ep_str = json.load(fp=f)
ikpys = my_json_encoder.decode(ep_str)
f.close()

if options.debug:
    print(".")

#Ouverture du fichier resultat
res_file = open("{}/{}/{}.res".format(MAIN_DIR, RES_DIR, name), "w")


##########################
# Execution de l'analyse #
##########################


for i in range(30):
    ###########################
    # Chargement du catalogue #
    ###########################

    filename = "{}/{}_{}.json".format(directory, name, i+1)

    if not os.path.isfile("{}.gz".format(filename)):
        print("File not found '{}.gz'.".format(filename), file=sys.stderr)
        continue
    
    #Chargement de la liste des observations du catalogue
    if options.debug:
        print()
        print("FILE : {}".format(i))
        print("Loading catalog")
    
    with gzip.open("{}.gz".format(filename), "rb") as f:
        ep_str = json.load(fp=f)
        end_points = my_json_encoder.decode(ep_str)

    nn = my_nearest_neighbor.RtreeNeighbor()

    poppy.set_nn(nn)
    grid.reset()

    if options.debug:
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
        if options.debug:
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
        grid.add_point(ep)


    ############################
    # Utilisation du catalogue #
    ############################

    #Calcul des distances aux buts
    if options.debug:
        print("Reaching goals           ")

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

    for gl, ik in zip(goals, ikpys):
        #Affichage de la barre de chargement
        if options.debug:
            if i%batch_size == 0 or i%1000 == 0:
                print("[", end='')
                for j in range(nb_batch-1):
                    if j < i/batch_size:
                        print("#", end='')
                    else:
                        print(" ", end='')
                print("] {}/{}".format(i,i_tot), end='\r')
            i=i+1
        #Execution du modele inverse sur le but
        posture = poppy.inv_model(gl)
        endpoint = poppy.get_end_point(posture)
        d = my_nearest_neighbor.dist(gl, endpoint.get_pos())

        res_gl.append(endpoint)
        dis_gl.append(d)

        #Execution du modele inverse sur ikpy(but)
        posture = poppy.inv_model(ik.get_pos())
        endpoint = poppy.get_end_point(posture)
        d = my_nearest_neighbor.dist(ik.get_pos(), endpoint.get_pos())

        res_ik.append(endpoint)
        dis_ik.append(d)

    del nn

    ##########################
    # Ecriture des resultats #
    ##########################

    if options.debug:
        print("Analysing results          ")

    distances_gl = numpy.array(dis_gl)
    distances_ik = numpy.array(dis_ik)

    remplissage = grid.nb_visited

    #remplissages
    res_file.write("{} ".format(grid.nb_visited / sphere_volume))
    if options.debug:
        print(grid.nb_visited / sphere_volume, end=" ")

    #volume
    pts = numpy.array([ep.get_pos() for ep in end_points])
    vol = scipy.spatial.ConvexHull(points=pts).volume
    res_file.write("{} ".format(vol))
    if options.debug:
        print(vol, end=" ")

    for array in [distances_gl, distances_ik]:
        #moyenne
        moy = array.mean()
        res_file.write("{} ".format(moy))
        if options.debug:
            print(moy, end=" ")

        #variance
        var = array.var()
        res_file.write("{} ".format(var))
        if options.debug:
            print(var, end=" ")

        #quartiles
        mi, q1, me, q3, ma = numpy.quantile(array, [0, 0.25, 0.5, 0.75, 1])
        res_file.write("{} {} {} {} {} ".format(mi, q1, me, q3, ma))
        if options.debug:
            print("{} {} {} {} {}".format(mi, q1, me, q3, ma), end=" ")

    res_file.write("\n")
    if options.debug:
        print()

res_file.close()
    