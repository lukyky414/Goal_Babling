import random
import my_robot
import my_nearest_neighbor
import my_goal_generation
from my_end_point import EndPoint

def Motor_Babling(robot : my_robot.Robot, steps=5000) -> list:
    """Execute un motor babling: positions aleatoires sur chacune des sections du robot.
    Retourne une deux listes: les positions obtenues, les angles utilises pour atteindre ces positions."""

    #Taille de barre de chargement
    nb_batch = 10

    #arrondis a l'inferieur
    batch_size = int(steps / nb_batch)
    if batch_size == 0:
        batch_size = 1

    end_points = []

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
        end_points.append(robot.get_end_point(angles=curr_angles))

    print("Motor Bablin done.      ")

    return end_points

def Goal_Babling(robot : my_robot.Robot, motor_babling_steps=5000, total_steps=10000):
    """Execute d'abord un motor babling, puis ameliore les connaissances avec un goal babling."""
    goals = []
    
    print("Motor Babling:")

    end_points = Motor_Babling(robot=robot, steps=motor_babling_steps)

    print("Goal Babling:")

    NN = my_nearest_neighbor.NearestNeighbor(end_points=end_points)

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
        goals.append(goal)

        nearest_end_point = NN.nearest(position=goal)

        new_posture = robot.randomize_posture(angles=nearest_end_point.get_posture())
        new_end_point = robot.get_end_point(angles=new_posture)

        NN.add_end_point(end_point=new_end_point)

        end_points.append(new_end_point)
        
    print("Goal Babling done.                 ")
    
    return end_points, goals
