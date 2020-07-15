from my_end_point import EndPoint

class Discretisation():
    def __init__(self, min = (-1, -1, -1), max = (1, 1, 1), precision = (200, 200, 200)):
        """Defini la taille des cellule de la discretisation.
        `min` donne le minimum pour les axes (x, y, z). Le minimum est compris dans la zone.
        `max` donne le maximum pour les axes (x, y, z). Le maximum est en dehors de la zone.
        `precision` donne le nombre de division des axes (x, y, z)."""

        #Le tableau contenant les données de la discrétisation
        self.table = [[[0
            for _ in range(precision[2])]
            for _ in range(precision[1])]
            for _ in range(precision[0])]
        self.precision = precision
        #les minimums et maximums
        self.min = min
        self.max = max
        #La taille d'une cellule selon chacun des axes
        self.size = (
            (max[0]-min[0]) / precision[0],
            (max[1]-min[1]) / precision[1],
            (max[2]-min[2]) / precision[2]
        )
        #Garde en mémoire les cellules visitées
        self.visited = []
    
    def get_cell(self, pos):
        for i in range(3):
            if pos[i] < 0 or pos[i] > self.precision[i]
                return 0
        
        return self.table[pos[0]][pos[1]][pos[2]]
    
    def get_discretized_pos(self, end_point : EndPoint):
        pos = end_point.get_pos()
        t = []

        good = True
        for i in range(3):
            if pos[i] < self.min[i] or pos[i] >= self.max[i]:
                good = False
                break
            t.append( math.floor(( pos[i] - self.min[i] ) / ( self.size[i] )) )

        if not good:
            return (-1, -1, -1)
        
        return t
    
    def add_point(self, end_point : EndPoint):
        """Prise en compte d'un nouveau end_point. Retourne 1 si le point est en dehors de la zone, 0 si pris en compte."""

        pos = self.grid.get_discretized_pos(end_point)
        if pos[0] != -1:
            if self.grid.get_cell() == 0:
                self.visited.append(pos)
            self.add_to_pos(pos)

        return 0
    
    def add_to_pos(self, pos):
        """Dans le cas où la position discrétisée a déjà été calculée"""
        self.table[pos[0]][pos[1]][pos[2]] += 1
    
    def reset(self):
        self.visited.clear()
        for tx in self.table:
            for ty in tx:
                for tz in ty:
                    tz = 0