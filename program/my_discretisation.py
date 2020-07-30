from my_end_point import EndPoint
import math

#Bien définir le min & max pour être sur et certain d'encadres entièrement le robot.
#Mieux vaut prévoir trop grand
#Par exemple, PoppyErgoJr a une taille d'environ 0.32. Cette grille peut prendre en charge un robot d'une taille jusqu'à 0.5
_MIN = (-0.5, -0.5, -0.5)
_MAX = (0.5, 0.5, 0.5)

# Je considère (0, 0, 0) la cellule qui a pour coins opposées les points: (0, 0, 0) et (cell_size, cell_size, cell_size)
class Discretisation():
    def __init__(self, cell_size : float):
        """Defini la taille des cellule de la discretisation."""
        self.min = _MIN
        self.max = _MAX

        # Nombre de cellules pour chacun des axes
        self.precision = [
            math.floor((ma-mi)/cell_size)+1
            for mi, ma in zip(self.min, self.max)
        ]

        # Le tableau contenant les données de la discrétisation
        self.table = [[[0
            for _ in range(self.precision[2])]
            for _ in range(self.precision[1])]
            for _ in range(self.precision[0])]
        # La taille d'une cellule
        self.size = cell_size
        # Garde en mémoire les cellules visitées
        self.visited = []
    
    def get_cell(self, pos):
        """Retourne le contenu d'une cellule de la discretisation. Retourne 0 si la cellule est hors memoire."""
        #Ici on prend en compte la portée de la mémoire car l'algo frontier peut dépasser la taille du robot, et donc la taille définie. Surtout si une cellule possède une grande taille.
        for i in range(3):
            if pos[i] < 0 or pos[i] >= self.precision[i] :
                return 0
        
        return self.table[pos[0]][pos[1]][pos[2]]
    
    def get_discretized_pos(self, end_point : EndPoint):
        """Retourne la position de la cellule contenant le end_point donné."""
        pos = end_point.get_pos()
        t = []

        good = True
        for i in range(3):
            t.append( math.floor(( pos[i] - self.min[i] ) / ( self.size )) )
        
        return t
    
    def add_point(self, end_point : EndPoint):
        """Prise en compte d'un nouveau end_point. Attentions aux points hors de portée."""
        #Pas de prise en charge des points hors de portée pour augmenter la rapidité de calcul
        pos = self.get_discretized_pos(end_point)
        if self.get_cell(pos) == 0:
            self.visited.append(pos)
        self.add_to_pos(pos)
    
    def add_to_pos(self, pos):
        """Dans le cas où la position discrétisée a déjà été calculée, pas besoin de faire add_point"""
        #Pas de prise en charge des points hors de portée pour augmenter la rapidité de calcul
        self.table[pos[0]][pos[1]][pos[2]] += 1