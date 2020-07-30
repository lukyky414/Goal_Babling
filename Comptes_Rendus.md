# Comptes rendus des réunions sur le projet

## Réunion vocale 19/06/2020 - 14h00

##### Concernant le projet:
Pour l'analyse, faire une discretisation par taille de cellule prédéfini (et non par ratio de la zone atteinte par le robot) pour pouvoir comparer les résultats d'algorithmes différents avec:
 * Le nombre de cellules visitées
 * Les différentes cellules visités dans l'un et non dans l'autre (visualisation possible en 3D)
Avec une taille prédéfinie il est possible de faire une évaluation en cours d'éxecution.

Pour mesurer les résultats, on peut:
 * Utiliser ikpy pour voir la différence de précision
 * Mesurer une différence sur les postures plutôt que sur les positions atteintes
 * Comparer deux modèles inverses avec la même liste de points/but généré soit aléatoirement, soit sur une grille
 * Générer une HeatMap sur l'erreur de précision en comparant avec des points sur une grille pour mettre en valeur les zones non atteintes
   -> Hypothèse : Une zone non explorée donne un taux d'erreur plus grand


##### Concernant le rapport:
 * Expliquer / introduire le plan du rapport pour être sûr d'aller dans la bonne direction
 * Détailler les algorithmes utilisés (écrire l'algorithme) comme Frontier, le suivi d'une droite, ...

Détails:
 * parindent / parskip : configurer la disposition d'un paragraphe
 * taille 11 : - [x] fait
 


## Réunion vocale 28/05/2020 - 14h00

La prise en compte de la rotation dans le projet est pour l'instant abandonnée.

##### Concernant le projet:
 * Préparer une discrétisation de l'espace 3D:
    * Méthode de génération de point selon l'algorithme `Frontier`
    * Métrique permettant de comparer les résultats de plusieurs algorithmes.
 * Terminer la méthode de génération `agnostique` de points ou un autre algorithme pour le comparer à `Frontier`
 * Mettre en place d'autre métriques permettant de comparer les résultats de différents algorithmes

##### Concernant le rapport:
Ajouter une explication des algorithmes utilisé pour avancer / remplir le rapport, ainsi que de poser à l'écrit une base pour les futures discussions. 



## Réunion vocale 06/05/2020 - 15h15

##### Dans un futur proche et concernant directement le code de l'application:
 * Vérifier les résultats obtenu avec le Nearest Neighbor utilisé part rapport aux résultats du projet de Fabien Benureau.
 * Ajouter une fonctionnalité pour appercevoir facilement la distribution des points dans l'espace 3D:
    * Avec différentes couleurs par rapport à la distance au centre
    * Avec un découpage par tranche, n'afficher que les points à une certaine distance du centre
    * En ajoutant des sphères / cercles pour pouvoir comparer celle-ci aux points

##### Points à travailler:
 * Nouvelles générations de but en s'inspirant des articles
 * Prendre en compte la rotation dans un but
 * Trouver une métrique qui permet de mesurer l'efficacité d'un algorithme:
   * Erreur moyenne sur un nombre de point généré aléatoirement
   * Distcrétisation de l'espace pour mesurer le taux de remplissage de celui-ci

Une fois que la métrique est en place et qu'au moins deux algorithmes ont été comparés, il y aura des questions à se poser et des variantes d'algorithmes à tester. Toute cette reflexion sera dans le rapport de stage.
