"""Fichier contenant les fonctions utiles à un apprentissage.
Principalement Motor Babling et Goal Babling."""

import random

def Motor_Babling(robot, steps=5000):
    """Execute un motor babling: positions aleatoires sur chacune des sections du robot.
    Retourne une deux listes: les positions obtenues, les angles utilisés pour atteindre ces positions."""

    #Taille de barre de chargement
    nb_batch = 10

    #arrondis à l'inferieur
    batch_size = int(steps / nb_batch)
    if batch_size == 0:
        batch_size = 1

    points = []

    angles = []

    for i in range(steps):
        #affichage barre de chargement
        if i%batch_size == 0:
            print("[", end='')
            for j in range(nb_batch):
                if j < i/batch_size:
                    print("#", end='')
                else:
                    print(" ", end='')
            print("]", end='\r')

        curr_angles = robot.random_angles()

        angles.append(curr_angles)

        robot.execute(curr_angles)

        pos = robot.end_point
        if len(pos) == 2:
            pos = (pos[0], pos[1], 0)

        points.append(pos)


    print("done", end='')
    for j in range(nb_batch-2):
        print(" ", end='')
    print()

    return points, angles

def Goal_Babling(robot, motor_babling_steps=5000, total_steps=10000):
    print("not defined.")