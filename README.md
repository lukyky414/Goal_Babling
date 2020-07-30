# Goal Babling

Basé sur <a href="https://github.com/benureau/recode/tree/master/benureau2015_gb">ce git</a>
Afin de créer un modèle inverse basée sur le remplissage d'une base de points connus et d'un NearestNeighbor, j'utilise plusieurs manières pour remplir cette base: principalement le GoalBabling avec une méthode spécifique pour le Goals On Grid qui est l'algorithme Frontier.

Ce projet fonctionne avec python 3 (3.8.5). J'utilise les bibliothèques suivantes. Celles-ci sont installées de base généralement:
`sys`, `os`, `math`, `random`, `numpy`, `argparse`

Celles-ci devront surement être installées [`pip install <Name>`].
`json`, `rtree`, `copy`, `pypot`, `pypot-creature`, `poppy-ergo-jr`

Tout ceci permet de faire tourner le programme. Maintenant, j'utilise d'autres bibliothèques pour l'affichage (non nécessaire si seul le script est lancé):
`pygame`, `pyopengl`, `matplotlib` (ainsi que `ctypes` qui devrait être présent de base)