from rtree import index
import sys
from my_end_point import EndPoint
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
    
    def nearest(self, position : tuple):
        """Retourne la posture se rapprochant le plus de la position demandée"""
        raise NotImplementedError

    def add_end_point(self, end_point : tuple):
        """Ajoute dans la base d'apprentissage du Nearest Neighbor le point donné"""
        raise NotImplementedError

    def reset(self, end_points : list):
        """Reset la base de recherhce avec une nouvelle liste d'end_points"""
        raise NotImplementedError



class RtreeNeighbor(NearestNeighbor):
    def __init__(self):
        self.my_rtree = None

    def nearest(self, position : tuple) -> EndPoint:
        # Normalement rtree fait une recherche par intersection de box (rectangle en 2d). Elle transforme une coordonnee seule en un rectangle de taille 0.
        # Pour empecher la modification du goal, on cree une copy de celui ci
        pos = copy.copy(position)
        # Meme en demandant un seul resultat, si deux points sont équidistant, la bibliothèque retournera 2 résultats.
        # Il faut donc transformer en liste
        posture_list = list(self.my_rtree.nearest(pos, num_results=1, objects='raw'))

        # Et retourner le 1e résultat
        return posture_list[0]

    def add_end_point(self, end_point : EndPoint):
        self.my_rtree.insert(id=self.nb_neighbor, coordinates=end_point.get_pos(), obj=end_point)
        self.nb_neighbor = self.nb_neighbor+1
    
    def reset(self, end_points):
        """Initialise le nearest neighbor avec un certain nombre de postures qui mènent à des positions 3D du robot."""

        if self.my_rtree is not None:
            del self.my_rtree
        # Initialisation de Rtree
        p = index.Property()
        p.dimension = 3
        self.my_rtree = index.Rtree(properties=p)

        # Ajout des points du motor bablind dans Rtree
        for i in range(len(end_points)):
            self.my_rtree.insert(id=i, coordinates=end_points[i].get_pos(), obj=end_points[i])
        self.nb_neighbor = len(end_points)



def test_neirest_neighboor(robot : my_robot.Robot, points_number = 5000, test_number=1000):
    diff = 0

    end_points = [(random.uniform(-1,1), random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(points_number)]

    NN = RtreeNeighbor()
    NN.reset(end_points)

    print("Testing nearest neighbor with simple method:")

    for i in range(test_number):
        # Barre de chargement
        print("[", end='')
        for j in range(19):
            if j < i/(test_number / 20):
                print("#", end='')
            else:
                print(" ", end='')
        print("] err: {} ".format(diff), end='\r')

        goal = [ random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1) ]

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