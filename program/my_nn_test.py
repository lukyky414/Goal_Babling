from my_nearest_neighbor import RtreeNeighbor, dist
import random
from my_end_point import EndPoint

#Permet de vérifier l'exactitude d'un Nearest Neighbor en utilisant une méthode naïve.

#Points in the base
points_number = 5000
#Number of tests
test_number=10000

#NN à tester
NN = RtreeNeighbor(True, f="TestNN")

#Compteur de différence de résultat
diff = 0

print("Generating points")

#Génération de points aléatoire
end_points = [EndPoint([], 
        (
            (0,0,0,random.uniform(-1,1)),
            (0,0,0,random.uniform(-1,1)),
            (0,0,0,random.uniform(-1,1)),
            (0,0,0,0)
        )
    ) for _ in range(points_number)
]

#Initialisation du nearest neighbor
NN.init(end_points)

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

    # Choix d'un but aléatoire
    goal = [ random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1) ]

    #Récupération du point le plus proche naivement
    naive_end_point = end_points[0]
    min_dist = dist(goal, end_points[0].get_pos())
    for p in end_points:
        pos = p.get_pos()
        d = dist(goal, pos)
        if d < min_dist:
            naive_end_point = p
            min_dist = d

    #Récupération du point le plus proche avec le nn
    nn_end_point = NN.nearest(goal)

    #Comparaison des points
    if not naive_end_point == nn_end_point:
        diff += 1

print("Test terminated with {} error(s). ({} % error)".format(diff, (100*diff/test_number)))