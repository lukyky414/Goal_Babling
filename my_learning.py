import random
import my_robot
import my_nearest_neighbor
import my_goal_generation

def Motor_Babling(robot : my_robot.Robot, steps=5000):
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

        curr_angles = robot.get_random_angles()

        angles.append(curr_angles)

        pos = my_robot.get_pos_from_matrix(matrix=robot.get_position(angles=curr_angles))

        if len(pos) == 2:
            pos = (pos[0], pos[1], 0)

        points.append(pos)

    print("done", end='')
    for j in range(nb_batch-2):
        print(" ", end='')
    print()

    return points, angles

def Goal_Babling(robot : my_robot.Robot, motor_babling_steps=5000, total_steps=10000):
    """Execute d'abord un motor babling, puis ameliore les connaissances avec un goal babling."""
    
    print("Motor Babling:")

    points, angles = Motor_Babling(robot=robot, steps=motor_babling_steps)

    print("Goal Babling:")

    NN = my_nearest_neighbor.NearestNeighbor(postures=angles, positions=points)

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

        goal = my_goal_generation.generate_goal(robot= robot)

        nearest_posture = NN.nearest(position=goal)

        new_posture = robot.randomize_posture(angles=nearest_posture)
        new_point = my_robot.get_pos_from_matrix(matrix=robot.get_position(angles=nearest_posture))

        NN.add_posture(posture=new_posture, position=new_point)

        angles.append(new_posture)
        points.append(new_point)

        
    print("done                      ")
    
    return points, angles
