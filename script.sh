# clear;

#Generer les dossiers et les fichiers de but / ikpy
# python program/0a_generate_directory.py
# python program/0b_generate_goals.py
# python program/0c_inv_model_ikpy.py

for step in 1000 100000; do #nb point dans catalogue
    #motor babling
    directory="files/Catalogues/motor_babling"
    for n in {1..30}; do
        options="--mb 1 --step $step --n $n"
        echo "python program/1_create_catalog.py $options"
    done

    #goal babling
    for pp in 0.05 0.2; do #perturbation posture
    for mb in 0.01 0.2; do #motor babling proportion

        #Agnostic
        directory="files/Catalogues/agnostic"
        for exp in 0.7 1.4; do #coef d'extansion
            for n in {1..30}; do
                options="--step $step --pp $pp --mb $mb --exp $exp --n $n --gg agnostic"
                echo "python program/1_create_catalog.py $options"
            done;
        done;

        #Frontier
        for nb_div in 10 1000; do #resolution discretisation
        for p_exp in 0.01 0.5 0.9; do #probabilité d'exploration
            for n in {1..30}; do
                options="--step $step --pp $pp --mb $mb --nb_div $nb_div --p_exp $p_exp --n $n --gg frontier"
                echo "python program/1_create_catalog.py $options"
            done;
        done; done;

    done; done;
done;

#Pour analyser tous les fichiers catalogues
# FILES=files/Catalogues/*.dat
# for f in $FILES; do
#     echo "python program/2_analyse_catalog $f";
# done
