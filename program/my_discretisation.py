from my_end_point import EndPoint
import math

#Bien définir le min & max pour être sur et certain d'encadres entièrement le robot.
#Mieux vaut prévoir trop grand
#Par exemple, PoppyErgoJr a une taille d'environ 0.32. Cette grille peut prendre en charge un robot d'une taille jusqu'à 0.5
_MIN = -0.5
_MAX = 0.5

# Je considère (0, 0, 0) la cellule qui a pour coins opposées les points: (0, 0, 0) et (cell_size, cell_size, cell_size)
class Discretisation():
    def __init__(self, nb_divs : float, save_visited : bool):
        """Defini la taille des cellule de la discretisation."""
        self.min = _MIN
        self.max = _MAX

        self.nb_divs = nb_divs
        self.nb_divs2 = nb_divs**2

        # Le tableau contenant les données de la discrétisation
        self.table = bytearray(math.floor(nb_divs**3 /8)+1)
        # La taille d'une cellule
        self.size = (self.max - self.min) / nb_divs
        self.save_visited = save_visited
        if save_visited:
            # Garde en mémoire les cellules visitées
            self.visited = []
        self.nb_visited = 0
    
    def get_cell(self, pos):
        """Retourne le contenu d'une cellule de la discretisation. Retourne 0 si la cellule est hors memoire."""
        #Ici on prend en compte la portée de la mémoire car l'algo frontier peut dépasser la taille du robot, et donc la taille définie. Surtout si une cellule possède une grande taille.
        for i in range(3):
            if pos[i] < 0 or pos[i] >= self.nb_divs :
                return 0
        
        n = pos[0]*self.nb_divs2 + pos[1]*self.nb_divs + pos[2]
        c = n>>3
        b = n&7

        return (self.table[c] & (1<<b)) > 0
    
    def get_discretized_pos(self, end_point : EndPoint):
        """Retourne la position de la cellule contenant le end_point donné."""
        pos = end_point.get_pos()
        t = []

        good = True
        for i in range(3):
            t.append( math.floor(( pos[i] - self.min ) / ( self.size )) )
        
        return t
    
    def add_point(self, end_point : EndPoint):
        """Prise en compte d'un nouveau end_point. Attentions aux points hors de portée."""
        #Pas de prise en charge des points hors de portée pour augmenter la rapidité de calcul
        pos = self.get_discretized_pos(end_point)
        if not self.get_cell(pos):
            if self.save_visited:
                self.visited.append(pos)
            self.nb_visited += 1
        self.add_to_pos(pos)
    
    def add_to_pos(self, pos):
        """Dans le cas où la position discrétisée a déjà été calculée, pas besoin de faire add_point"""
        #Pas de prise en charge des points hors de portée pour augmenter la rapidité de calcul
        n = pos[0]*self.nb_divs2 + pos[1]*self.nb_divs + pos[2]
        c = n>>3
        b = n&7

        self.table[c] = self.table[c] | 1<<b
    
    def reset(self):
        del self.table
        self.table = bytearray(math.floor(self.nb_divs**3 /8)+1)
        self.nb_visited = 0