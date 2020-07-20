import matplotlib.pyplot as plt
import math
from my_robot import Robot
from my_nearest_neighbor import NearestNeighbor
from my_discretisation import Discretisation


def test_neirest_neighboor(NN : NearestNeighbor, points_number = 5000, test_number=1000):
    diff = 0

    end_points = [(random.uniform(-1,1), random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(points_number)]

    NN.reset(end_points)

    print("Testing nearest neighbor with naive method:")

    for i in range(test_number):
        # Barre de chargement
        print("[", end='')
        for j in range(19):
            if j < i/(test_number / 20):
                print("#", end='')
            else:
                print(" ", end='')
        print("] err: {} ".format(diff), end='\r')

        goal = [ random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1) ]

        naive_end_point = end_points[0]
        min_dist = dist(goal, end_points[0].get_pos())

        for p in end_points:
            pos = p.get_pos()
            d = dist(goal, pos)
            if d < min_dist:
                naive_end_point = p
                min_dist = d

        nn_end_point = NN.nearest(goal)

        if not naive_end_point == nn_end_point:
            diff += 1
    
    print("Test terminated with {} error(s). ({} % error)".format(diff, (100*diff/test_number)))

    return diff

def difference_discretisation(grid1 : Discretisation, grid2 : Discretisation):
    """Retourne les cellules populées dans grid1 mais non grid2"""
    res = []
    for cell in grid1.visited:
        if grid2.get_cell(cell) == 0:
            res.append(cell)
    
    return res

def errors(robot : Robot, goals : list):
    """Retourne la liste des distances entre les goals et les points retournés par le modèle inverse du robot """
    dist = []
    
    for goal in goals:
        near = robot.inv_model(goal)
        dist.append(near)

    return dist

def plots_distribution(robot : Robot, endpoints : list, precision = 100):
    """Cree trois plot pour chacun des axes et affiche la distribution des points sur ces aces"""

    xs = [0] * precision
    ys = [0] * precision
    zs = [0] * precision
    dists = []
        
    mi_x = robot.bounds[0][0]
    ma_x = robot.bounds[0][1]
    mi_y = robot.bounds[1][0]
    ma_y = robot.bounds[1][1]
    mi_z = robot.bounds[2][0]
    ma_z = robot.bounds[2][1]
    max_d = robot.furthest
    
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
        
        xs[x_index] += 1
        ys[y_index] += 1
        zs[z_index] += 1
        
        d = 0
        for p in ep.get_pos():
            d += p**2
        d = math.sqrt(d)
        dists.append(d)

    axe_x = []
    axe_y = []
    axe_z = []
    for i in range(precision):
        axe_x.append(i * (ma_x - mi_x) / precision + mi_x)
        axe_y.append(i * (ma_y - mi_y) / precision + mi_y)
        axe_z.append(i * (ma_z - mi_z) / precision + mi_z)
    
    graph = [0] * precision
    for d in dists:
        index = math.floor(precision*d/max_d)
        if index == precision:
            index -= 1
        graph[index] += 1

    _, plots = plt.subplots(4)
    plots[0].plot(axe_x, xs)
    plots[0].set_ylabel("Number of points")
    plots[0].set_xlabel("X coordinates")
    plots[1].plot(axe_y, ys)
    plots[1].set_ylabel("Number of points")
    plots[1].set_xlabel("Y coordinates")
    plots[2].plot(axe_z, zs)
    plots[2].set_ylabel("Number of points")
    plots[2].set_xlabel("Z coordinates")
    plots[3].plot(dists, graph)
    plots[3].set_ylabel("Number of points")
    plots[3].set_xlabel("Distance from origin")
    plt.show()