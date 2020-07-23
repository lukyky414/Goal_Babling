import sys

if __name__ != "__main__":
    print("This file needs to be run as main")
    sys.exit(1)

import random

import my_robot
import my_learning
import my_goal_generation
import my_discretisation
import my_nearest_neighbor
import my_option

#Récupération des options & paramètres
options = my_option.get_options()

#Création du nom de fichier en fonction des paramètres
if options.mb == 1 and options.gg != "none":
    raise "Cannot use a goal generator if using only motor babling"

if options.gg == "none":
    if options.mb != 1:
        raise "Cannot use `none` goal generator if using goal babling"
    name = "MotorBabling_"
else:
    name = "GoalBabling-{}MotorBabling_{}_".format(options.mb,options.gg)
    if options.gg == "agnostic":
        name += "{}".format(options.exp)
    elif options.gg == "frontier":
        name += "{}p-{}cell".format(options.p_exp, options.size)

name += "_{}step_{}disturb".format(options.steps, options.pp)

if options.n is not None:
    name += "_{}".format(options.n)


#Création du robot
poppy = my_robot.Robot()

#Le seed chane après la création d'une pypot.creature. Réinitialisation nécessaire après la création du robot.
random.seed(options.seed)

end_points, goals = None, None
nn = None

nn = my_nearest_neighbor.RtreeNeighbor(save_load=True, name=name)

if options.mb == 1:
    end_points, goals = my_learning.Motor_Babling(
        robot=poppy,
        steps=options.steps,
        printing=options.debug
    )

    nn.init(end_points)
else:
    gg = None

    if options.gg == "agnostic":
        gg = my_goal_generation.AgnosticGenerator(robot=poppy, coef=options.exp)
    elif options.gg == "frontier":
        grid = my_discretisation.Discretisation(cell_size=options.size)
        gg = my_goal_generation.FrontierGenerator(p=options.p_exp, grid=grid)
    
    if gg is None:
        raise "Please select a valid goal generator"

    end_points, goals = my_learning.Goal_Babling(
        robot=poppy,
        NN=nn,
        GG=gg,
        steps=options.steps,
        motor_babling_proportion=options.mb,
        perturbation=options.pp,
        printing=options.debug
    )