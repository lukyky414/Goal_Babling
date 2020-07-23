from my_end_point import EndPoint
import math

_MIN = (-0.5, -0.5, -0.5)
_MAX = (0.5, 0.5, 0.5)

class Discretisation():
    def __init__(self, cell_size = 0.01):
        """Defini la taille des cellule de la discretisation.
        `min` donne le minimum pour les axes (x, y, z). Le minimum est compris dans la zone.
        `max` donne le maximum pour les axes (x, y, z). Le maximum est en dehors de la zone.
        `precision` donne le nombre de division des axes (x, y, z)."""

        self.precision = [
            (ma-mi)/cell_size
            for mi, ma in zip(_MIN, _MAX)
        ]

        #Le tableau contenant les données de la discrétisation
        self.table = [[[0
            for _ in range(self.precision[2])]
            for _ in range(self.precision[1])]
            for _ in range(self.precision[0])]
        #La taille d'une cellule
        self.size = cell_size
        #Garde en mémoire les cellules visitées
        self.visited = []
    
    def get_cell(self, pos):
        for i in range(3):
            if pos[i] < 0 or pos[i] > self.precision[i] :
                return 0
        
        return self.table[pos[0]][pos[1]][pos[2]]
    
    def get_discretized_pos(self, end_point : EndPoint):
        pos = end_point.get_pos()
        t = []

        good = True
        for i in range(3):
            t.append( math.floor(( pos[i] - _MIN[i] ) / ( self.size )) )
        
        return t
    
    def add_point(self, end_point : EndPoint):
        """Prise en compte d'un nouveau end_point. Retourne 1 si le point est en dehors de la zone, 0 si pris en compte."""

        pos = self.get_discretized_pos(end_point)
        if self.get_cell(pos) == 0:
            self.visited.append(pos)
        self.add_to_pos(pos)

        return 0
    
    def add_to_pos(self, pos):
        """Dans le cas où la position discrétisée a déjà été calculée"""
        self.table[pos[0]][pos[1]][pos[2]] += 1
    
    def reset(self):
        self.visited.clear()
        self.table = [[[0
            for _ in range(self.precision[2])]
            for _ in range(self.precision[1])]
            for _ in range(self.precision[0])]