from rtree import index
import sys

class NearestNeighbor:
    def __init__(self, postures : list, positions : list):
        """Initialise le nearest neighbor avec un certain nombre de postures qui mènent à des positions 3D du robot."""

        if len(postures) != len(positions) : 
            print("[ERR] - NearestNeighbor __init__ : postures et positions n'ont pas la même taille.", file=sys.stderr)
            sys.exit(1)

        # Initialisation de Rtree
        p = index.Property()
        p.dimension = 3
        self.my_rtree = index.Rtree(properties=p)

        # Ajout des points du motor bablind dans Rtree
        for i in range(len(positions)):
            self.my_rtree.insert(id=i, coordinates=positions[i], obj=postures[i])
        self.nb_neighbor = len(positions)
    
    def nearest(self, position : tuple):
        """Retourne la posture se rapprochant le plus de la position demandée"""
        # Meme en demandant un seul resultat, si deux points sont équidistant, la bibliothèque retournera 2 résultats.
        # Il faut donc transformer en liste
        posture_list = list(self.my_rtree.nearest(position, num_results=1, objects='raw'))

        # Et retourner le 1e résultat
        return posture_list[0]

    def add_posture(self, posture : list, position : tuple):
        """Ajoute dans la base d'apprentissage du Nearest Neighbor le point donné"""
        self.my_rtree.insert(id=self.nb_neighbor, coordinates=position, obj=posture)
        self.nb_neighbor = self.nb_neighbor+1
