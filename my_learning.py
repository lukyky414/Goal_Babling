from __future__ import print_function
import random
import my_robot
from ikpy.chain import Chain
from rtree import index

def Motor_Babling(robot, steps=5000):
    """Execute un motor babling: positions aleatoires sur chacune des sections du robot.
    Retourne une deux listes: les positions obtenues, les angles utilises pour atteindre ces positions."""

    #Taille de barre de chargement
    nb_batch = 10

    #arrondis a l'inferieur
    batch_size = int(steps / nb_batch)
    if batch_size == 0:
        batch_size = 1

    points = []

    angles = []

    for i in range(steps):
        #affichage barre de chargement
        if i%batch_size == 0:
            print("[", end='')
            for j in range(nb_batch-1):
                if j < i/batch_size:
                    print("#", end='')
                else:
                    print(" ", end='')
            print("]", end='\r')

        curr_angles = my_robot.get_random_posture_angles(robot=robot)

        angles.append(curr_angles)

        pos = my_robot.get_position(robot=robot, angles=curr_angles)

        if len(pos) == 2:
            pos = (pos[0], pos[1], 0)

        points.append(pos)

    print("done", end='')
    for j in range(nb_batch-2):
        print(" ", end='')
    print()

    return points, angles

def Goal_Babling(robot, motor_babling_steps=5000, total_steps=10000):
    """Execute d'abord un motor babling, puis ameliore les connaissances avec un goal babling."""
    
    print("Motor Babling:")

    points, angles = Motor_Babling(robot=robot, steps=motor_babling_steps)

    print("Goal Babling:")

    p = index.Property()
    p.dimension = 3
    neighbors = index.Rtree(properties=p)

    for i in range(len(points)):
        neighbors.insert(id=i, coordinates=points[i], obj=angles[i])
    nb_neighbor = len(points)

    #Taille de barre de chargement
    nb_batch = 20

    #arrondis a l'inferieur
    batch_size = int((total_steps-motor_babling_steps) / nb_batch)
    if batch_size == 0:
        batch_size = 1

    for i in range(total_steps-motor_babling_steps):
        #affichage barre de chargement
        if i%batch_size == 0:
            print("[", end='')
            for j in range(nb_batch-1):
                if j < i/batch_size:
                    print("#", end='')
                else:
                    print(" ", end='')
            print("]", end='\r')

        goal = [
            random.uniform(-robot._length, robot._length),
            random.uniform(-robot._length, robot._length),
            random.uniform(-robot._length, robot._length)
        ]

        # Methode lente
        # nearest_posture = nearest_neighbor_posture(goal, points, angles)

        nearest_posture = list(neighbors.nearest(goal, num_results=1, objects='raw'))[0]

        new_posture = my_robot.randomize_posture(robot, nearest_posture)
        new_point = my_robot.get_position(robot=robot, angles=nearest_posture)

        neighbors.insert(nb_neighbor, new_point, new_posture)
        nb_neighbor = nb_neighbor+1

        angles.append(new_posture)
        points.append(new_point)
    print("done                      ")
    
    return points, angles

def dist(a, b):
    return sum((a_i-b_i)**2 for a_i, b_i in zip(a, b))


def nearest_neighbor_posture(goal, points, angles):
    """Trouve le points le plus proche du goal et retourne la posture associee"""

    min_dist = float('inf')
    posture = None

    for i in range(len(points)):
        d = dist(goal, points[i])
        if d < min_dist:
            min_dist = d
            posture = angles[i]
    
    return posture
