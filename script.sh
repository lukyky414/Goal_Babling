clear;
#Options generales pour toutes executions
options="--gg agnostic --seed 0 --steps 100"
#Options par rapport aux user input
#options = "$options $@"

#Sur quelle option il faut boucler
for exp in 0.2 0.8 1 1.1 1.3 1.4 1.5 1.7 1.9 2 5 10 50
do
    #Options pour ce parcour de boucle (ajouter la variable de la boucle)
    this_option="$options --exp $exp"
    #Recuperer le nom du fichier qui sera genere et utilise pour le reste
    name=$(python main_learning.py --getname $this_option);
    #Afficher le nom pour suivre l'execution du script
    echo $name
    #Lancement du programme et des analyses
    python main_learning.py $this_option;
    python main_inverse_model.py $name;
    python main_analysis.py $name;
    #Affichage du resultat d'execution
    cat files/AnalysisResult/$name.json;
    #Echo parce que la fin de fichier n'a pas de retour a la ligne
    echo;
done