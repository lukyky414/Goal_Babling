import matplotlib.pyplot as plt
import math

from my_robot import Robot
from my_nearest_neighbor import NearestNeighbor, dist
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
        posture = robot.inv_model(goal)
        pos = robot.get_end_point(posture).get_pos()
        d = dist(goal, pos)
        dist.append(d)

    return dist

def plots_distribution(endpoints : list, precision = 100):
    """Cree trois plot pour chacun des axes et affiche la distribution des points sur ces aces"""

    xs = [0] * precision
    ys = [0] * precision
    zs = [0] * precision
    ds = [0] * precision
        
    mi_x = endpoints[0].get_pos()[0]
    ma_x = endpoints[0].get_pos()[0]
    mi_y = endpoints[1].get_pos()[1]
    ma_y = endpoints[1].get_pos()[1]
    mi_z = endpoints[2].get_pos()[2]
    ma_z = endpoints[2].get_pos()[2]
    ma_d = dist((0, 0, 0), endpoints[0].get_pos())

    nb = len(endpoints)
    
    for ep in endpoints:
        pos = ep.get_pos()
        d = dist((0, 0, 0), pos)

        if pos[0] < mi_x:
            mi_x = pos[0]
        if pos[0] > ma_x:
            ma_x = pos[0]

        if pos[1] < mi_y:
            mi_y = pos[1]
        if pos[1] > ma_y:
            ma_y = pos[1]

        if pos[2] < mi_z:
            mi_z = pos[2]
        if pos[2] > ma_z:
            ma_z = pos[2]
        
        if d > ma_d:
            ma_d = d

    step_x = (ma_x-mi_x)/precision
    step_y = (ma_y-mi_y)/precision
    step_z = (ma_z-mi_z)/precision
    step_d = (ma_d)/precision


    for ep in endpoints:
        x, y, z = ep.get_pos()
        d = dist((0, 0, 0), (x, y, z))

        x_index = math.floor(precision*(x-mi_x)/(ma_x-mi_x))
        y_index = math.floor(precision*(y-mi_y)/(ma_y-mi_y))
        z_index = math.floor(precision*(z-mi_z)/(ma_z-mi_z))
        d_index = math.floor(precision*(   d  )/(   ma_d  ))

        if x_index == precision:
            x_index -= 1
        if y_index == precision:
            y_index -= 1
        if z_index == precision:
            z_index -= 1
        if d_index == precision:
            d_index -= 1
        
        xs[x_index] += 1
        ys[y_index] += 1
        zs[z_index] += 1
        ds[d_index] += 1

    axe_x = []
    axe_y = []
    axe_z = []
    axe_d = []
    for i in range(precision):
        axe_x.append(i * step_x + mi_x)
        axe_y.append(i * step_y + mi_y)
        axe_z.append(i * step_z + mi_z)
        axe_d.append(i * step_d       )
        


    plt.plot(axe_x, xs)
    plt.ylabel("Number of points")
    plt.xlabel("X coordinates")

    plt.figure()
    plt.plot(axe_y, ys)
    plt.ylabel("Number of points")
    plt.xlabel("Y coordinates")

    plt.figure()
    plt.plot(axe_z, zs)
    plt.ylabel("Number of points")
    plt.xlabel("Z coordinates")

    plt.figure()
    plt.plot(axe_d, ds)
    plt.ylabel("Number of points")
    plt.xlabel("Distance from origin")

    plt.show()