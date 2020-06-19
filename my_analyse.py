import matplotlib.pyplot as plt
import math
from my_robot import Robot
import my_nearest_neighbor
import my_goal_generation

def discretization(endpoints : list, min = (-1, -1, -1), max = (1, 1, 1), precision = 100, table = None, start = 0):
    """Retourne un tableau, résultat de la discretisation de l'espace, chaque cellule ayant le nombre de endpoints contenu dans son espace.Les limites sont le minimum et maximum de chaques axes (-x, -y, -z), (x, y, z). La taille d'une cellule est à préciser.
    On peut donner un tableau deja pré-rempli en donnant le numéro du premier point à analyser (start)"""

    if table is None:
        table = [[[0 for _ in range(precision)] for _ in range(precision)] for _ in range(precision)]
    nb = ((max[0]-min[0]) / precision, (max[1]-min[1]) / precision, (max[2]-min[2]) / precision)
    #print(nb)
    t = [0]*3

    for ep in endpoints[start:]:
        pos = ep.get_pos()

        good = True
        for i in range(3):
            if pos[i] < min[i] or pos[i] > max[i]:
                good = False
                break
            t[i] = math.floor(( pos[i] - min[i] ) / ( nb[i] ))

        if not good:
            continue
        

        #print("{} -> {}".format(pos, t))

        table[t[0]][t[1]][t[2]] += 1
    
    return table

def error(robot : Robot, endpoints : list, precision = 5000):
    """Retourne la distance moyenne entre un goal généré aléatoirement et le point retourné par le modèle inverse (nearest neighbor)"""
    NN = my_nearest_neighbor.NearestNeighbor(endpoints)
    dist = 0
    for _ in range(precision):
        goal = my_goal_generation.generate_goal(robot, coef=1)
        near = NN.nearest(goal).get_pos()

        dist += my_nearest_neighbor.dist(goal, near)

    dist = dist / precision

    return dist


def plot_dist_to_origin(robot : Robot, endpoints : list, precision = 100):
    """Pose sur un plot la distribution par rapport à la distance à l'origine du repère"""

    dists = []
    max_d = robot.furthest
    for ep in endpoints:
        d = 0
        for p in ep.get_pos():
            d += p**2
        d = math.sqrt(d)
        dists.append(d)

    graph = [0]*precision
    for d in dists:
        index = math.floor(precision*d/max_d)
        if index == precision:
            index -= 1
        graph[index] += 1
    
    dists = []
    for i in range(precision):
        dists.append(i*max_d/precision)
    
    plt.plot(dists, graph)
    plt.ylabel("number of point")
    plt.xlabel("distance from origin")
    plt.show()

def plot_x_y_z_distribution(robot : Robot, endpoints : list, precision = 100):
    """Cree trois plot pour chacun des axes et affiche la distribution des points sur ces aces"""

    xs = [0 for _ in range(precision)]
    ys = [0 for _ in range(precision)]
    zs = [0 for _ in range(precision)]
        
    mi_x = robot.bounds[0][0]
    ma_x = robot.bounds[0][1]
    mi_y = robot.bounds[1][0]
    ma_y = robot.bounds[1][1]
    mi_z = robot.bounds[2][0]
    ma_z = robot.bounds[2][1]
    
    for ep in endpoints:
        x, y, z = ep.get_pos()
        x_index = math.floor(precision*(x-mi_x)/(ma_x-mi_x))
        y_index = math.floor(precision*(y-mi_y)/(ma_y-mi_y))
        z_index = math.floor(precision*(z-mi_z)/(ma_z-mi_z))

        if x_index == precision:
            x_index -= 1
        if y_index == precision:
            y_index -= 1
        if z_index == precision:
            z_index -= 1
        
        if show:
            xs[x_index] += 1
            ys[y_index] += 1
            zs[z_index] += 1
    
    axe_x = []
    axe_y = []
    axe_z = []
    for i in range(precision):
        axe_x.append(i * (ma_x - mi_x) / precision + mi_x)
        axe_y.append(i * (ma_y - mi_y) / precision + mi_y)
        axe_z.append(i * (ma_z - mi_z) / precision + mi_z)
        

    _, plots = plt.subplots(3)
    plots[0].plot(axe_x, xs)
    plots[0].set_ylabel("Number of points")
    plots[0].set_xlabel("X coordinates")
    plots[1].plot(axe_y, ys)
    plots[1].set_ylabel("Number of points")
    plots[1].set_xlabel("Y coordinates")
    plots[2].plot(axe_z, zs)
    plots[2].set_ylabel("Number of points")
    plots[2].set_xlabel("Z coordinates")
    plt.show()