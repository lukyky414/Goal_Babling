
import random
import math

from my_robot import Robot
from my_end_point import EndPoint
from my_discretisation import Discretisation


class GoalGenerator:
    def __init__(self):
        """Classe mere."""
    
    def newGoal(self):
        """Fonction qui generera un goal. A definir dans les classes filles"""
        raise NotImplementedError

    def addGoal(self, goal):
        """Lorsqu'un but a été retenu par l'apprentissage"""
        raise NotImplementedError

    def add_end_point(self, end_point : EndPoint):
        """Lorsqu'un EndPoint a été atteint pendant l'apprentissage"""
        raise NotImplementedError
    
    def init(self, end_points : list):
        """Initialise le générateur de but avec cette liste d'end_points"""
        raise NotImplementedError

class AgnosticGenerator(GoalGenerator):
    def __init__(self, robot : Robot, coef : int):
        """Initialise le générateur de but agnostic en précisant quel sera le coefficient d'aggrandissement de l'espace de but."""
        self.coef = coef
        self.bounds = None
    
    def newGoal(self):
        """Génère un but dans l'espace défini"""
        #On prend les limites atteintes
        axe_x, axe_y, axe_z = self.bounds
        
        #Quelques calculs pour agrandir l'espace sur chacun des axes
        demi_size_x = (axe_x[1]-axe_x[0])/2
        demi_size_y = (axe_y[1]-axe_y[0])/2
        demi_size_z = (axe_z[1]-axe_z[0])/2

        mid_x = demi_size_x + axe_x[0]
        mid_y = demi_size_y + axe_y[0]
        mid_z = demi_size_z + axe_z[0]

        add_x = demi_size_x * self.coef
        add_y = demi_size_y * self.coef
        add_z = demi_size_z * self.coef

        goal = (
            random.uniform(mid_x-add_x, mid_x+add_x),
            random.uniform(mid_y-add_y, mid_y+add_y),
            random.uniform(mid_z-add_z, mid_z+add_z)
        )

        return goal

    def addGoal(self, goal):
        return
    
    def add_end_point(self, end_point):
        pos = end_point.get_pos()
        for i in range(3):
            if pos[i] < self.bounds[i][0]:
                self.bounds[i][0] = pos[i]
            if pos[i] > self.bounds[i][1]:
                self.bounds[i][1] = pos[i]

    def init(self, end_points):
        pos = end_points[0].get_pos()
        self.bounds = [[pos[0], pos[0]], [pos[1], pos[1]], [pos[2], pos[2]]]

        for ep in end_points:
            self.add_end_point(ep)

class GoalOnGridGenerator(GoalGenerator):
    def __init__(self, p, grid:Discretisation):
        """Classe mere pour generer un point sur une grille en utilisant le p-reached strategy"""
        self.p = p
        self.grid = grid
    
    def newGoalOutside(self):
        """Genere un nouveau but dans une cellule non exploree"""
        raise NotImplementedError
    
    def newGoal(self):
        """Génère un nouveau but."""
        r = random.random()
        #Avec une proba p, le but sera en dehors des cellules visitées
        if r < self.p:
            return self.newGoalOutside()
        #Avec une proba 1-p, le but sera dans une cellule déjà visitée
        else:
            return self.newGoalInside()
    
    def newGoalInside(self):
        """Genere un nouveau but dans une cellule deja exploree"""
        cell = random.choice(self.grid.visited)
        return self.newGoalFromCell(cell)

    def newGoalFromCell(self, pos):
        """Génère un but aléatoirement dans une cellule définie"""
        return (
            random.uniform(pos[0]*self.grid.size+self.grid.min,(pos[0]+1)*self.grid.size+self.grid.min), 
            random.uniform(pos[1]*self.grid.size+self.grid.min,(pos[1]+1)*self.grid.size+self.grid.min), 
            random.uniform(pos[2]*self.grid.size+self.grid.min,(pos[2]+1)*self.grid.size+self.grid.min)
        )

    def addGoal(self, goal):
        return
    
    def add_end_point(self, end_point):
        self.grid.add_point(end_point)
    
    def init(self, end_points):
        for ep in end_points:
            self.add_end_point(ep)     

class FrontierGenerator(GoalOnGridGenerator):
    def __init__(self, p : float, grid : Discretisation):
        """Le Rtree est utilisé pour executer une recherche par cellule."""
        super(FrontierGenerator, self).__init__(p=p, grid=grid)
        self.end_points = []

    #Pas de self, avoir une direction aléatoire peut se faire sans instantiation d'objet FrontierGenerator
    def get_random_dir():
        """Choisir une direction aleatoire en 3d"""

        # https://mathworld.wolfram.com/SpherePointPicking.html
        u = random.uniform(0,1)
        v = random.uniform(0,1)

        theta = 2*math.pi*u
        phi = math.acos(2*v-1)

        x = math.cos(theta) * math.sin(phi)
        y = math.sin(theta) * math.sin(phi)
        z = math.cos(phi)

        # #Distribution gaussienne sur chacune des dimensions
        # vec = [random.gauss(0, 1) for _ in range(3)]

        # #Normaliser le vecteur
        # mag = sum(x**2 for x in vec) ** .5
        # dir = [x/mag for x in vec]

        return (x, y, z)

    def newGoalOutside(self):
        #choisir aleatoirement un point de depart
        ep = random.choice(self.end_points)
        pos = ep.get_pos()
        size = self.grid.size

        #Choisir une direction aleatoire
        dir = FrontierGenerator.get_random_dir()

        # coordonnee du point de départ dans l'espace discretisé
        (x, y, z) = self.grid.get_discretized_pos(ep)

        # determine la direction du vecteur dir dans chacun des axes
        dx = 1 if dir[0] > 0 else -1
        dy = 1 if dir[1] > 0 else -1
        dz = 1 if dir[2] > 0 else -1

        # Distance à parcourir sur le vecteur dir pour changer de cellule, à partir du bord d'une cellule
        # mx -> Max distance à parcourir sur axe X avant de changer de position discrète
        mx = (size / (dir[0])) * dx
        my = (size / (dir[1])) * dy
        mz = (size / (dir[2])) * dz

        # Distance à parcourir sur le vecteur dir pour changer de cellule, à partir de la position actuelle
        # nx -> Next distance à parcourir sur axe X avant de changer de position discrète 
        # Je récupère la position dans la cellule
        #       if dx == 1 : size - pos[0]%size
        #       else: pos[0]%size
        # Je prend la position relative dans la cellule
        #       / size
        # J'applique cette position relative (~ = proportion) à la distance max
        #       * mx
        nx = ( (size*(dx+1)/2) - dx*(pos[0]%size) ) / size * mx
        ny = ( (size*(dy+1)/2) - dy*(pos[1]%size) ) / size * my
        nz = ( (size*(dz+1)/2) - dz*(pos[2]%size) ) / size * mz

        # Suivre la direction avant de s'arreter
        is_ended = False
        while ( not is_ended ):
            
            # Recherche de la distance minimum pour un changement de position
            if nx < ny:
                # X min
                if nx < nz:
                    d = nx #La distance à parcourir sur dir avant de changer de position en X
                    nx = mx #Le prochain changement en X se fera après une distance de mx
                    ny -= d #On parcour la distance d. Prise en compte donc pour les compteurs Y
                    nz -= d #  et Z
                    x += dx #Mise à jours de la position X
                # Z min
                else :
                    d = nz
                    nz = mz
                    nx -= d
                    ny -= d
                    z += dz
            else:
                #Y min
                if ny < nz:
                    d = ny
                    ny = my
                    nx -= d
                    nz -= d
                    y += dy
                #Z min
                else :
                    d = nz
                    nz = mz
                    nx -= d
                    ny -= d
                    z += dz
                
            # cellule vide -> fin de boucle
            if self.grid.get_cell((x, y, z)) == 0:
                is_ended = True
        
        #Generer un point dans cette cellule vide
        return self.newGoalFromCell((x, y, z))
    
    
    def init(self, end_points):
        super().init(end_points)
        #Sauvegarde du pointeur sur les EndPoints
        self.end_points = end_points
