import sys

if __name__ != "__main__":
    print("This file needs to be run as main", file=sys.stderr)
    sys.exit(1)

import random
import os
import json

import my_robot
import my_learning
import my_goal_generation
import my_discretisation
import my_nearest_neighbor
import my_option
import my_json_encoder

DIRECTORY = "files/NearestNeighbor"

#Dossier des fichiers
name = ""

#Récupération des options & paramètres
options = my_option.get_options_learning()

#Création du nom de fichier en fonction des paramètres
if options.mb == 1:
    options.gg = None

if options.gg is None:
    if options.mb != 1:
        print("Cannot use `none` goal generator if using goal babling (mb!=0, gg==none)", file=sys.stderr)
        sys.exit(1)
    name += "MotorBabling_"
else:
    name += "GoalBabling-{}MotorBabling_{}_".format(options.mb,options.gg)
    if options.gg == "agnostic":
        name += "{}_".format(options.exp)
    elif options.gg == "frontier":
        name += "{}p-{}cell_".format(options.p_exp, options.size)

name += "{}step_{}disturb".format(options.steps, options.pp)

if options.n is not None:
    name += "_{}".format(options.n)

if options.getname:
    print(name)
    sys.exit(0)


#Création du robot
poppy = my_robot.Robot()

#Le seed chane après la création d'une pypot.creature. Réinitialisation nécessaire après la création du robot.
random.seed(options.seed)

end_points, goals = None, None
nn = None

#save_load=True --> Saving in a new file (override old one if exist)
if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)
nn = my_nearest_neighbor.RtreeNeighbor(save_load=True, f="{}/{}".format(DIRECTORY,name))

#Motor Babling only
if options.mb == 1:
    end_points = my_learning.Motor_Babling(
        robot=poppy,
        steps=options.steps,
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
        grid = my_discretisation.Discretisation(cell_size=options.size)
        gg = my_goal_generation.FrontierGenerator(p=options.p_exp, grid=grid)
    
    if gg is None:
        print("Please select a valid goal generator", file=sys.stderr)
        sys.exit(1)

    #Execution de l'apprentissage
    end_points, goals = my_learning.Goal_Babling(
        robot=poppy,
        NN=nn,
        GG=gg,
        steps=options.steps,
        motor_babling_proportion=options.mb,
        perturbation=options.pp,
        printing=options.debug
    )

if options.debug:
    print("Saving end_points")

f = open("{}/{}_ep.json".format(DIRECTORY, name), "w")
json.dump(end_points, fp=f, cls=my_json_encoder.EP_Encoder)
f.close()

if options.debug:
    print("Saving goals")

f = open("{}/{}_g.json".format(DIRECTORY, name), "w")
json.dump(goals, fp=f)
f.close()