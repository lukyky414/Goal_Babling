import random
import my_robot
from ikpy.chain import Chain
# import learners

def Motor_Babling(robot: Chain, steps=5000):
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

def Goal_Babling(robot: Chain, motor_babling_steps=5000, total_steps=10000):
    """Execute d'abord un motor babling, puis ameliore les connaissances avec un goal babling."""
    
    print("Motor Babling:")

    points, angles = Motor_Babling(robot=robot, steps=motor_babling_steps)

    print("Goal Babling:")

    #Taille de barre de chargement
    nb_batch = 20

    #arrondis à l'inferieur
    batch_size = int((total_steps-motor_babling_steps) / nb_batch)
    if batch_size == 0:
        batch_size = 1

    for i in range(total_steps-motor_babling_steps):
        #affichage barre de chargement
        if i%batch_size == 0:
            print("[", end='')
            for j in range(nb_batch):
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

        nearest = nearest_neighbor_posture(goal, points, angles)

        posture = my_robot.randomize_posture(robot, nearest)

        angles.append(posture)
        points.append(my_robot.get_position(robot=robot, angles=posture))
    
    return points, angles

def dist(a, b):
    return sum((a_i-b_i)**2 for a_i, b_i in zip(a, b))

# _nn_set = learners.NNSet()

def nearest_neighbor_posture(goal: list, points: list, angles: list):
    """Trouve le points le plus proche du goal et retourne la posture associee"""

    # global _nn_set
    # history = zip(points, angles)
    
    # if len(points) < len(_nn_set):
    #     _nn_set = learners.NNSet()

    # for i in range(len(_nn_set), len(points)):
    #     _nn_set.add(angles[i], y=points[i])
    
    # idx = _nn_set.nn_y(goal)[1][0]
    
    # return angles[idx]

    min_dist = float('inf')
    posture = None

    for i in range(len(points)):
        d = dist(goal, points[i])
        if d < min_dist:
            min_dist = d
            posture = angles[i]
    
    return posture
