# Comptes rendus des réunions sur le projet

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
