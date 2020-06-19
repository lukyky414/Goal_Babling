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

# Je considère (0, 0, 0) la cellule qui a pour coins opposées les points: (0, 0, 0) et (cell_size, cell_size, cell_size)
class GoalOnGridGenerator(GoalGenerator):
    def __init__(self, cell_size = 0.1, p = 0.5):
        """Classe mere pour generer un point sur une grille en utilisant le p-reached strategy"""
        self.cell_size = cell_size
        self.p = p
    
    def newGoalOutside(self):
        """Genere un nouveau but dans une cellule non exploree"""
        raise NotImplementedError
    
    def newGoal(self):
        r = random.random()
        if r > p:
            self.newGoalOutside()
        else:
            self.newGoalInside()
    
    def newGoalInside(self):
        """Genere un nouveau but dans une cellule deja exploree"""
        
    def addGoal(self, goal):
        return
    
    def add_end_point(self, end_point):
        # Les endpoints sont deja ajoutes a end_points (qui est un pointeur vers le tableau)
        return
    
    def reset(self, end_points):
        #TODO enregistrer les cellules visitees
        return
        

class FrontierGenerator(GoalOnGridGenerator):
    def __init__(self, RT : my_nearest_neighbor.RtreeNeighbor, cell_size = 0.1, p =0.5):
        """Le Rtree est utilisé pour executer une recherche par cellule."""
        super(FrontierGenerator, self).__init__(cell_size=cell_size, p=p)
        self.rt = RT
        self.end_points = None


    def newGoalOutside(self):
        #choisir aleatoirement un point de depart
        ep = random.choice(self.end_points)

        #Choisir une direction aleatoire en 3d
        vec = [random.gauss(0, 1) for i in range(3)]
        mag = sum(x**2 for x in vec) ** .5
        dir = [x/mag for x in vec]

        # coordonnee du point actuel dans l'espace discretisé
        x = math.floor(ep.posture[0] / self.cell_size)
        y = math.floor(ep.posture[1] / self.cell_size)
        z = math.floor(ep.posture[2] / self.cell_size)

        # determine la direction du vecteur dir dans chacun des axes
        dx = 1 if dir[0] > 0 else -1
        dy = 1 if dir[1] > 0 else -1
        dz = 1 if dir[2] > 0 else -1

        # distance a parcourir sur le vecteur 'dir' avant de changer de coordonnee dans l'espace discret à partir du point ep
        nx = (x + size * dx - ep.posture[0]) / dir[0]
        ny = (y + size * dy - ep.posture[1]) / dir[1]
        nx = (x + size * dz - ep.posture[2]) / dir[2]

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
            # TODO utiliser la liste des cellules visitees de la classe mere
                # temporaire
            #Rechercher les cellules correspondantes dans rtree
            list(
                self.rt.my_rtree.intersection(
                    x*size, y*size, z*size, (x+1)*size, (y+1)*size, (z+1)*size
                )
            )
            if list.count() == 0:
                is_ended = True
                # fin temporaire
        
        #Generer un point dans cette cellule
        return (random.uniform(x*size,(x+1)*size), random.uniform(y*size,(y+1)*size), random.uniform(z*size,(z+1)*size))
    
    
    def reset(self, end_points):
        super().reset(end_points)
        self.end_points = end_points
