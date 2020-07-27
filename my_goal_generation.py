
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
        """Ajouter un but retenu (visé)  dans la base"""
        raise NotImplementedError

    def add_end_point(self, end_point : EndPoint):
        """Ajouter un nouvel end_point ou une liste de end_points dans la base de recherche"""
        raise NotImplementedError
    
    def init(self, end_points : list):
        """Initialise le générateur de but avec cette liste d'end_points"""
        raise NotImplementedError

class AgnosticGenerator(GoalGenerator):
    def __init__(self, robot : Robot, coef : int):
        """Initialise le générateur de but agnostic en précisant quel robot sera utilisé et quel sera le coefficient d'aggrandissement de l'espace de but."""
        self.robot = robot
        self.coef = coef
        self.bounds = None
    
    def newGoal(self):
        size_x, size_y, size_z = self.bounds

        goal = (
            random.uniform(size_x[0] * self.coef, size_x[1] * self.coef),
            random.uniform(size_y[0] * self.coef, size_y[1] * self.coef),
            random.uniform(size_z[0] * self.coef, size_z[1] * self.coef)
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

# Je considère (0, 0, 0) la cellule qui a pour coins opposées les points: (0, 0, 0) et (cell_size, cell_size, cell_size)
class GoalOnGridGenerator(GoalGenerator):
    def __init__(self, p, grid:Discretisation):
        """Classe mere pour generer un point sur une grille en utilisant le p-reached strategy"""
        self.p = p
        self.grid = grid
    
    def newGoalOutside(self):
        """Genere un nouveau but dans une cellule non exploree"""
        raise NotImplementedError
    
    def newGoal(self):
        r = random.random()
        if r < self.p:
            return self.newGoalOutside()
        else:
            return self.newGoalInside()
    
    def newGoalInside(self):
        """Genere un nouveau but dans une cellule deja exploree"""
        cell = random.choice(self.grid.visited)
        return self.newGoalFromCell(cell)

    def newGoalFromCell(self, pos):
        return (
            random.uniform(pos[0]*self.grid.size+self.grid.min[0],(pos[0]+1)*self.grid.size+self.grid.min[0]), 
            random.uniform(pos[1]*self.grid.size+self.grid.min[1],(pos[1]+1)*self.grid.size+self.grid.min[1]), 
            random.uniform(pos[2]*self.grid.size+self.grid.min[2],(pos[2]+1)*self.grid.size+self.grid.min[2])
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
        self.end_points = None

    def get_random_dir():
        #Choisir une direction aleatoire en 3d
        vec = [random.gauss(0, 1) for i in range(3)]
        mag = sum(x**2 for x in vec) ** .5
        dir = [x/mag for x in vec]

        return dir

    def newGoalOutside(self):
        #choisir aleatoirement un point de depart
        ep = random.choice(self.end_points)
        pos = ep.get_pos()

        dir = FrontierGenerator.get_random_dir()

        # coordonnee du point actuel dans l'espace discretisé
        p = self.grid.get_discretized_pos(ep)
        x = p[0]
        y = p[1]
        z = p[2]

        # determine la direction du vecteur dir dans chacun des axes
        dx = 1 if dir[0] > 0 else -1
        dy = 1 if dir[1] > 0 else -1
        dz = 1 if dir[2] > 0 else -1

        # distance a parcourir sur le vecteur 'dir' avant de changer de coordonnee dans l'espace discret à partir du point ep
        nx = (x + self.grid.size * dx - pos[0]) / dir[0]
        ny = (y + self.grid.size * dy - pos[1]) / dir[1]
        nz = (z + self.grid.size * dz - pos[2]) / dir[2]

        # distance maximale a parcourir sur le vecteur 'dir' avant d'etre sûr de changer de coordonne dans l'espace discret à partir de n'importe quel point
        mx = 1 / dir[0]
        my = 1 / dir[1]
        mz = 1 / dir[2]


        is_ended = False
        while ( not is_ended ):

            #Appliquer equation de droite pour avoir la coordonnee de la prochaine cellule visitee
            if nx < ny:
                if nx < nz:
                    d = nx
                    nx = mx
                    ny -= d
                    nz -= d
                    x += dx
                else :
                    d = nz
                    nz = mz
                    nx -= d
                    ny -= d
                    z += dz
            else:
                if ny < nz:
                    d = ny
                    ny = my
                    nx -= d
                    nz -= d
                    y += dy
                else :
                    d = nz
                    nz = mz
                    nx -= d
                    ny -= d
                    z += dz
                
            # cellule vide -> fin de boucle
            if self.grid.get_cell((x, y, z)) == 0:
                is_ended = True
        
        #Generer un point dans cette cellule
        return self.newGoalFromCell((x, y, z))
    
    
    def init(self, end_points):
        super().init(end_points)
        self.end_points = end_points
