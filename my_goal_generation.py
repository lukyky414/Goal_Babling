import my_robot
import my_end_point
import random
import math
import my_nearest_neighbor
import my_discretisation


class GoalGenerator:
    def __init__(self):
        """Classe mere."""
    
    def newGoal(self):
        """Fonction qui generera un goal. A definir dans les classes filles"""
        raise NotImplementedError

    def addGoal(self, goal):
        """Ajouter un but retenu (visé)  dans la base"""
        raise NotImplementedError

    def add_end_point(self, end_point : my_end_point.EndPoint):
        """Ajouter un nouvel end_point ou une liste de end_points dans la base de recherche"""
        raise NotImplementedError
    
    def reset(self, end_points : list):
        """Réinitialise le générateur de but avec cette nouvelle liste d'end_points"""
        raise NotImplementedError

class AgnosticGenerator(GoalGenerator):
    def __init__(self, robot : my_robot.Robot, coef=1.4):
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
        if self.bounds is None:
            self.bounds = [[pos[0], pos[0]], [pos[1], pos[1]], [pos[2], pos[2]]]
        else:
            for i in range(3):
                if pos[i] < self.bounds[i][0]:
                    self.bounds[i][0] = pos[i]
                if pos[i] > self.bounds[i][1]:
                    self.bounds[i][1] = pos[i]

    def reset(self, end_points):
        self.size_x = [0, 0]
        self.size_y = [0, 0]
        self.size_z = [0, 0]

        for ep in end_points:
            self.add_end_point(ep)

# Je considère (0, 0, 0) la cellule qui a pour coins opposées les points: (0, 0, 0) et (cell_size, cell_size, cell_size)
class GoalOnGridGenerator(GoalGenerator):
    def __init__(self, p, min, max, precision):
        """Classe mere pour generer un point sur une grille en utilisant le p-reached strategy"""
        self.p = p
        self.grid = my_discretisation.Discretisation(min=min, max=max, precision=precision)
    
    def newGoalOutside(self):
        """Genere un nouveau but dans une cellule non exploree"""
        raise NotImplementedError
    
    def newGoal(self):
        r = random.random()
        if r > self.p:
            return self.newGoalOutside()
        else:
            return self.newGoalInside()
    
    def newGoalInside(self):
        """Genere un nouveau but dans une cellule deja exploree"""
        cell = random.choice(self.grid.visited)
        return self.newGoalFromCell(cell)

    def newGoalFromCell(self, pos):
        return (
            random.uniform(pos[0]*self.grid.size[0]+self.grid.min[0],(pos[0]+1)*self.grid.size[0]+self.grid.min[0]), 
            random.uniform(pos[1]*self.grid.size[1]+self.grid.min[1],(pos[1]+1)*self.grid.size[1]+self.grid.min[1]), 
            random.uniform(pos[2]*self.grid.size[2]+self.grid.min[2],(pos[2]+1)*self.grid.size[2]+self.grid.min[2])
        )

    def addGoal(self, goal):
        return
    
    def add_end_point(self, end_point):
        self.grid.add_point(end_point)
    
    def reset(self, end_points):
        self.grid.reset()
        for ep in end_points:
            self.add_end_point(ep)
        

class FrontierGenerator(GoalOnGridGenerator):
    def __init__(self, p = 0.5, min = (-1, -1, -1), max = (1, 1, 1), precision = (200, 200, 200)):
        """Le Rtree est utilisé pour executer une recherche par cellule."""
        super(FrontierGenerator, self).__init__(p=p, min=min, max=max, precision=precision)
        self.end_points = None


    def newGoalOutside(self):
        #choisir aleatoirement un point de depart
        ep = random.choice(self.end_points)
        pos = ep.get_pos()

        #Choisir une direction aleatoire en 3d
        vec = [random.gauss(0, 1) for i in range(3)]
        mag = sum(x**2 for x in vec) ** .5
        dir = [x/mag for x in vec]

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
        nx = (x + self.grid.size[0] * dx - pos[0]) / dir[0]
        ny = (y + self.grid.size[1] * dy - pos[1]) / dir[1]
        nz = (z + self.grid.size[2] * dz - pos[2]) / dir[2]

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
    
    
    def reset(self, end_points):
        super().reset(end_points)
        self.end_points = end_points
