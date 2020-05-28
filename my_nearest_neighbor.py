from rtree import index
import sys
from my_end_point import EndPoint
import my_goal_generation
import my_robot
import my_learning
from math import sqrt
import random
import copy

def dist(A, B):
    res = 0
    for a, b in zip(A, B):
        res += (a-b)**2
    return sqrt(res)

class NearestNeighbor:
    def __init__(self, end_points : list):
        """Initialise le nearest neighbor avec un certain nombre de postures qui mènent à des positions 3D du robot."""
        # Initialisation de Rtree
        p = index.Property()
        p.dimension = 3
        self.my_rtree = index.Rtree(properties=p)

        # Ajout des points du motor bablind dans Rtree
        for i in range(len(end_points)):
            self.my_rtree.insert(id=i, coordinates=end_points[i].get_pos(), obj=end_points[i])
        self.nb_neighbor = len(end_points)

    def nearest(self, position : tuple) -> EndPoint:
        """Retourne la posture se rapprochant le plus de la position demandée"""
        # Normalement rtree fait une recherche par intersection de box (rectangle en 2d). Elle transforme une coordonnee seule en un rectangle de taille 0.
        # Pour empecher la modification du goal, on cree une copy de celui ci
        pos = copy.copy(position)
        # Meme en demandant un seul resultat, si deux points sont équidistant, la bibliothèque retournera 2 résultats.
        # Il faut donc transformer en liste
        posture_list = list(self.my_rtree.nearest(pos, num_results=1, objects='raw'))

        # Et retourner le 1e résultat
        return posture_list[0]

    def add_end_point(self, end_point : EndPoint):
        """Ajoute dans la base d'apprentissage du Nearest Neighbor le point donné"""
        self.my_rtree.insert(id=self.nb_neighbor, coordinates=end_point.get_pos(), obj=end_point)
        self.nb_neighbor = self.nb_neighbor+1


def test_neirest_neighboor(robot : my_robot.Robot, points_number = 5000, test_number=1000):
    diff = 0

    end_points = my_learning.Motor_Babling(robot=robot, steps=points_number)

    NN = NearestNeighbor(end_points)

    print("Testing nearest neighbor with simple method:")

    for i in range(test_number):
        print("[", end='')
        for j in range(19):
            if j < i/(test_number / 20):
                print("#", end='')
            else:
                print(" ", end='')
        print("] err: {} ".format(diff), end='\r')

        goal = [ random.choice([-1, 1]), random.choice([-1, 1]), random.choice([-1, 1]) ]

        naive_end_point = end_points[0]
        min_dist = dist(goal, end_points[0].get_pos())

        for p in end_points:
            pos = p.get_pos()
            d = dist(goal, pos)
            if d < min_dist:
                naive_end_point = p
                min_dist = d

        nn_end_point = NN.nearest(goal)

        if not naive_end_point == nn_end_point:
            diff += 1
    
    print("Test terminated with {} error(s). ({} % error)".format(diff, (100*diff/test_number)))

    return diff