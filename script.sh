clear;
#Options generales pour toutes executions
options="--seed 0 --gg frontier --steps 100000"
# options="--seed 0 --gg frontier"
#Options par rapport aux user input
#options = "$options $@"

#Sur quelle option il faut boucler
for X in 0 0.1 0.2 0.3 0.4 0.6 0.7 0.8 0.9 1
do
    #Options pour ce parcour de boucle (ajouter la variable de la boucle)
    this_option="$options --p_exp $X"
    #Recuperer le nom du fichier qui sera genere et utilise pour le reste
    name=$(python program/main_learning.py --getname $this_option);
    #Afficher le nom pour suivre l'execution du script
    echo $name
    #Lancement du programme et des analyses
    python program/main_learning.py $this_option;
    python program/main_inverse_model.py $name;
    python program/main_analysis.py $name;
    #Affichage du resultat d'execution
    cat files/AnalysisResult/$name.json;
    #Echo parce que la fin de fichier n'a pas de retour a la ligne
    echo;
done