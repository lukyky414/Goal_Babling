import my_robot
import my_end_point
import random
import math
import my_nearest_neighbor

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
    
    def newGoal(self):
        size_x, size_y, size_z = self.robot.bounds

        goal = (
            random.uniform(size_x[0] * self.coef, size_x[1] * self.coef),
            random.uniform(size_y[0] * self.coef, size_y[1] * self.coef),
            random.uniform(size_z[0] * self.coef, size_z[1] * self.coef)
        )

        return goal

    def addGoal(self, goal):
        return
    
    def add_end_point(self, end_point):
        return

    def reset(self, end_points):
        return
        

class FrontierGenerator(GoalGenerator):
    def __init__(self, cell_size : 0.1, NN : my_nearest_neighbor.RtreeNeighbor):
        """Le Rtree est utilisé pour executer une recherche par cellule."""
        self.cell_size = cell_size
        self.end_points = []
    
    def newGoal(self):
        ep = random.choice(self.end_points)
        #Choisir une direction
        #Appliquer equation de droite
        #Rechercher les cellules correspondantes dans rtree
        #s'arreter a la 1e cellule vide
        #Generer un point dans cette cellule
        
    def addGoal(self, goal):
        return
    
    def add_end_point(self, end_point):
        self.end_points.append(end_point)
    
    def reset(self, end_points):
        self.end_points = end_points.copy()
