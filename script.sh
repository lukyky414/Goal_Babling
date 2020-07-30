clear;
#Options generales pour toutes executions
options="--seed 0 --gg frontier --steps 100000 --mb 0.2"
#Options par rapport aux user input
#options = "$options $@"

#Sur quelle option il faut boucler
for pert in 0.01 0.1 1 10
do
    #Options pour ce parcour de boucle (ajouter la variable de la boucle)
    this_option="$options --pp $pert"
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