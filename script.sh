clear;

#Generer fichiers des goals
if ! test -f "files/Goals.json"; then
    python program/0a_generate_goals.py
fi

#Options generales pour toutes executions
gen_option="--gg frontier"

#Options par rapport aux user input
#options = "$options $@"

#Sur quelle option il faut boucler
for X in 0 0.2 0.4 0.6 0.8
do
    #Options pour ce parcour de boucle (ajouter la variable de la boucle)
    loop_option="$gen_option --mb $X"

    for n in {1..15}; do
        echo
        echo $n
        
        #Ajouter la valeur de n dans les options
        this_option="$loop_option --n $n"

        #Recuperer le nom du fichier qui sera genere et utilise pour le reste
        name=$(python program/1_learn_inverse_model.py --getname $this_option --nodebug);

        #Lancement du programme et des analyses
        python program/1_learn_inverse_model.py $this_option;
        echo
        python program/2_use_inverse_model.py $name;
        echo
        python program/3_analyse_inverse_model_results.py $name;
    done
done