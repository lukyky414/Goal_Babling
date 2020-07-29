import random
import math

from my_robot import Robot
from my_nearest_neighbor import NearestNeighbor
from my_goal_generation import GoalGenerator

#Caractere pour effacer la ligne au dessus
erase = '\x1b[1A\x1b[2K'


def Motor_Babling(robot : Robot, steps : int, printing : bool) -> list:
    """Execute un motor babling: positions aleatoires sur chacune des sections du robot.
    Retourne une deux listes: les positions obtenues, les angles utilises pour atteindre ces positions."""

    if printing:
        print("Motor Babling:")

    robot.reset()

    if printing:
        #Taille de barre de chargement
        nb_batch = 10

        #arrondis a l'inferieur
        batch_size = int(steps / nb_batch)
        if batch_size == 0:
            batch_size = 1

    end_points = []

    for i in range(steps):
        #affichage barre de chargement
        if printing and i%batch_size == 0:
            print("[", end='')
            for j in range(nb_batch-1):
                if j < i/batch_size:
                    print("#", end='')
                else:
                    print(" ", end='')
            print("] {}/{}".format(i,steps), end='\r')

        curr_angles = robot.get_random_angles()
        end_points.append(robot.get_end_point(angles=curr_angles))

    if printing:
        print(erase + "Motor Babling: done.")
        print("                                    ", end='\r')

    return end_points

def Goal_Babling(robot : Robot, NN : NearestNeighbor, GG : GoalGenerator, steps : int, motor_babling_proportion : float, perturbation : float, printing : bool):
    """Execute d'abord un motor babling, puis ameliore les connaissances avec un goal babling."""
    
    motor_babling_steps = math.floor(steps * motor_babling_proportion)+1
    goal_babling_steps = steps - motor_babling_steps

    #Fait un reset du robot.
    end_points = Motor_Babling(robot=robot, steps=motor_babling_steps, printing=printing)


    if printing:
        print("Goal Babling:")

    NN.init(end_points)
    GG.init(end_points)
    goals = []

    if printing:
        #Taille de barre de chargement
        nb_batch = 20

        #arrondis a l'inferieur
        batch_size = int((steps-motor_babling_steps) / nb_batch)
        if batch_size == 0:
            batch_size = 1

    for i in range(goal_babling_steps):
        #affichage barre de chargement
        if printing and i%batch_size == 0:
            print("[", end='')
            for j in range(nb_batch-1):
                if j < i/batch_size:
                    print("#", end='')
                else:
                    print(" ", end='')
            print("] {}/{}".format(i,goal_babling_steps), end='\r')

        goal = GG.newGoal()
        goals.append(goal)
        GG.addGoal(goal)

        nearest_end_point = NN.nearest(position=goal)

        new_posture = robot.randomize_posture(angles=nearest_end_point.get_posture(), perturbation = perturbation)
        new_end_point = robot.get_end_point(angles=new_posture)

        NN.add_end_point(end_point=new_end_point)
        GG.add_end_point(end_point=new_end_point)

        end_points.append(new_end_point)
    
    if printing:
        print(erase + "Goal Babling: done.")
        print("                                         ", end='\r')
    
    return end_points, goals
