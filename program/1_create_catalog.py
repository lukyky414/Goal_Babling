import sys

if __name__ != "__main__":
    print("This file needs to be run as main", file=sys.stderr)
    sys.exit(1)

import random
import os
import json

from my_files_paths import *
import my_robot
import my_learning
import my_goal_generation
import my_discretisation
import my_nearest_neighbor
import my_option
import my_json_encoder
import my_name_generator

#Récupération des options & paramètres
options = my_option.get_options_learn()

if options.debug:
    print("Step1:Learning Inverse Model")

#Création du nom de fichier en fonction des paramètres
name = my_name_generator.get_file_name(options)
directory = "{}/{}".format(MAIN_DIR, CTL_DIR)

if options.getname:
    print(name)
    sys.exit(0)

if options.debug:
    print(name)
    print("Initialising")

#Création du robot
poppy = my_robot.Robot()

#Le seed chane après la création d'une pypot.creature. Réinitialisation nécessaire après la création du robot.
random.seed(options.seed)

end_points, goals = None, None
nn = None

for end in [".dat", ".idx", "_ep.json", "_g.json"]:
    filename = "{}/{}{}".format(directory, name, end)
    if os.path.exists(filename):
        os.remove(filename)

nn = my_nearest_neighbor.RtreeNeighbor(f="{}/{}".format(directory,name))

if options.debug:
    print("Learning")

#Motor Babling only
if options.mb == 1:
    end_points = my_learning.Motor_Babling(
        robot=poppy,
        steps=options.step,
        printing=options.debug
    )
    #Pas de but à suivre pour le motor babling
    goals = []
    #Enregistrement nécessaire dans le nn
    nn.init(end_points)
else:
    gg = None

    #Choix du goal generator
    if options.gg == "agnostic":
        gg = my_goal_generation.AgnosticGenerator(robot=poppy, coef=options.exp)
    elif options.gg == "frontier":
        grid = my_discretisation.Discretisation(nb_divs=options.nb_div, save_visited=True)
        gg = my_goal_generation.FrontierGenerator(p=options.p_exp, grid=grid)
    
    if gg is None:
        print("Please select a valid goal generator", file=sys.stderr)
        sys.exit(1)

    #Execution de l'apprentissage
    end_points, goals = my_learning.Goal_Babling(
        robot=poppy,
        NN=nn,
        GG=gg,
        steps=options.step,
        motor_babling_proportion=options.mb,
        perturbation=options.pp,
        printing=options.debug
    )

if options.debug:
    print("Saving end_points")

f = open("{}/{}_ep.json".format(directory, name), "w")
json.dump(end_points, fp=f, cls=my_json_encoder.EP_Encoder)
f.close()

if options.debug:
    print("Saving goals")

f = open("{}/{}_g.json".format(directory, name), "w")
json.dump(goals, fp=f)
f.close()