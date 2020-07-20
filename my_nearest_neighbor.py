from rtree import index
import sys
from my_end_point import EndPoint
from math import sqrt
import copy


def dist(A, B):
    res = 0
    for a, b in zip(A, B):
        res += (a-b)**2
    return sqrt(res)

class NearestNeighbor:
    
    def nearest(self, position : tuple):
        """Retourne l'endpoint se rapprochant le plus de la position demandée"""
        raise NotImplementedError

    def nearest_list(self, position : tuple, num_results : int):
        """Retourne la liste d'endpoint les plus proches de la position demandée"""
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

    def nearest(self, position : tuple):
        res = self.nearest_list(position=position, num_results=1)
        return res[0]
    
    def nearest_list(self, position : tuple, num_results : int):
        # Normalement rtree fait une recherche par intersection de box (rectangle en 2d). Elle transforme une coordonnee seule en un rectangle de taille 0.
        # Pour empecher la modification du goal, on cree une copy de celui ci
        pos = copy.copy(position)

        # Meme en demandant un seul resultat, si deux points sont équidistant, la bibliothèque retournera 2 résultats.
        # Il faut donc transformer en liste même si on ne demande qu'un seul résultat
        posture_list = list(self.my_rtree.nearest(pos, num_results=num_results, objects='raw'))
        return posture_list


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