import matplotlib.pyplot as plt
import matplotlib
import numpy
import os
import re
import subprocess
import json
import sys
from scipy.stats import mannwhitneyu

from my_files_paths import *
import my_option
import my_name_generator
import my_json_encoder

def get_statistic_diff(arr1, arr2):
    _, p = mannwhitneyu(arr1, arr2)

    if p < 0.0001:
        return "****"
    elif p < 0.001:
        return "***"
    elif p < 0.01:
        return "**"
    elif p < 0.05:
        return "*"
    return "N D"


FOLDER = "{}/{}".format(MAIN_DIR, RES_DIR)

##################################
########### FIRST STEP ###########
##################################
name = "1*mb*100000*"
box_1 = "Motor Babling"

output = subprocess.check_output("ls {}/{}".format(FOLDER, name), shell=True)
files = output.decode('ascii')

files = files.splitlines()

#remplissage, couver, {moy, var, mi, q1, me, q3, ma} * gl & ik
tab_res1 = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

for f in files:
    fo = open(f, "r")
    lines = fo.read().splitlines()
    for l in lines:
        val = l.split(" ")
        for i in range(16):
            tab_res1[i].append(float(val[i]))

rempli_1 = numpy.array(tab_res1[0])
couver_1 = numpy.array(tab_res1[1])
gl_moy_1 = numpy.array(tab_res1[2])
gl_var_1 = numpy.array(tab_res1[3])
gl_min_1 = numpy.array(tab_res1[4])
gl_qa1_1 = numpy.array(tab_res1[5])
gl_med_1 = numpy.array(tab_res1[6])
gl_qa3_1 = numpy.array(tab_res1[7])
gl_max_1 = numpy.array(tab_res1[8])
ik_moy_1 = numpy.array(tab_res1[9])
ik_var_1 = numpy.array(tab_res1[10])
ik_min_1 = numpy.array(tab_res1[11])
ik_qa1_1 = numpy.array(tab_res1[12])
ik_med_1 = numpy.array(tab_res1[13])
ik_qa3_1 = numpy.array(tab_res1[14])
ik_max_1 = numpy.array(tab_res1[15])

###################################
########### SECOND STEP ###########
###################################
name = "*.2mb*100000*agnos*1.4e*"
box_2 = "Agnostic"

output = subprocess.check_output("ls {}/{}".format(FOLDER, name), shell=True)
files = output.decode('ascii')

files = files.splitlines()

#remplissage, couver, {moy, var, mi, q1, me, q3, ma} * gl & ik
tab_res2 = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

for f in files:
    fo = open(f, "r")
    lines = fo.read().splitlines()
    for l in lines:
        val = l.split(" ")
        for i in range(16):
            tab_res2[i].append(float(val[i]))

rempli_2 = numpy.array(tab_res2[0])
couver_2 = numpy.array(tab_res2[1])
gl_moy_2 = numpy.array(tab_res2[2])
gl_var_2 = numpy.array(tab_res2[3])
gl_min_2 = numpy.array(tab_res2[4])
gl_qa1_2 = numpy.array(tab_res2[5])
gl_med_2 = numpy.array(tab_res2[6])
gl_qa3_2 = numpy.array(tab_res2[7])
gl_max_2 = numpy.array(tab_res2[8])
ik_moy_2 = numpy.array(tab_res2[9])
ik_var_2 = numpy.array(tab_res2[10])
ik_min_2 = numpy.array(tab_res2[11])
ik_qa1_2 = numpy.array(tab_res2[12])
ik_med_2 = numpy.array(tab_res2[13])
ik_qa3_2 = numpy.array(tab_res2[14])
ik_max_2 = numpy.array(tab_res2[15])

##################################
########### THIRD STEP ###########
##################################
name = "*.2mb*100000*fro*.5pe*10r*"
box_3 = "Frontier"

output = subprocess.check_output("ls {}/{}".format(FOLDER, name), shell=True)
files = output.decode('ascii')

files = files.splitlines()

#remplissage, couver, {moy, var, mi, q1, me, q3, ma} * gl & ik
tab_res3 = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

for f in files:
    fo = open(f, "r")
    lines = fo.read().splitlines()
    for l in lines:
        val = l.split(" ")
        for i in range(16):
            tab_res3[i].append(float(val[i]))

rempli_3 = numpy.array(tab_res3[0])
couver_3 = numpy.array(tab_res3[1])
gl_moy_3 = numpy.array(tab_res3[2])
gl_var_3 = numpy.array(tab_res3[3])
gl_min_3 = numpy.array(tab_res3[4])
gl_qa1_3 = numpy.array(tab_res3[5])
gl_med_3 = numpy.array(tab_res3[6])
gl_qa3_3 = numpy.array(tab_res3[7])
gl_max_3 = numpy.array(tab_res3[8])
ik_moy_3 = numpy.array(tab_res3[9])
ik_var_3 = numpy.array(tab_res3[10])
ik_min_3 = numpy.array(tab_res3[11])
ik_qa1_3 = numpy.array(tab_res3[12])
ik_med_3 = numpy.array(tab_res3[13])
ik_qa3_3 = numpy.array(tab_res3[14])
ik_max_3 = numpy.array(tab_res3[15])



#################################
########### RESULTATS ###########
#################################

matplotlib.rcParams["savefig.directory"] = os.chdir(os.path.dirname("/projects/stage_m2/rapport/graphics/"))

text = "MB-Agn:{} | Agn-Fro: {} | MB-Fro:{}"

plt.figure("Remplissage")
# plt.title(get_statistic_diff(rempli_1,rempli_2))
# plt.boxplot([rempli_1, rempli_2])
# plt.xticks([1, 2] , [box_1, box_2])
plt.title( text.format(
    get_statistic_diff(rempli_1,rempli_2),
    get_statistic_diff(rempli_2,rempli_3),
    get_statistic_diff(rempli_1,rempli_3)
))
plt.boxplot([rempli_1, rempli_2, rempli_3])
plt.xticks([1, 2, 3] , [box_1, box_2, box_3])

plt.figure("Couverture")
# plt.title(get_statistic_diff(couver_1,couver_2))
# plt.boxplot([couver_1, couver_2])
# plt.xticks([1, 2] , [box_1, box_2])
plt.title( text.format(
    get_statistic_diff(couver_1,couver_2),
    get_statistic_diff(couver_2,couver_3),
    get_statistic_diff(couver_1,couver_3)
))
plt.boxplot([couver_1, couver_2, couver_3])
plt.xticks([1, 2, 3] , [box_1, box_2, box_3])



plt.figure("Moyenne Goals")
# plt.title(get_statistic_diff(gl_moy_1,gl_moy_2))
# plt.boxplot([gl_moy_1, gl_moy_2])
# plt.xticks([1, 2] , [box_1, box_2])
plt.title( text.format(
    get_statistic_diff(gl_moy_1,gl_moy_2),
    get_statistic_diff(gl_moy_2,gl_moy_3),
    get_statistic_diff(gl_moy_1,gl_moy_3)
))
plt.boxplot([gl_moy_1, gl_moy_2, gl_moy_3])
plt.xticks([1, 2, 3] , [box_1, box_2, box_3])

# plt.figure("Variance Goals")
# plt.title(get_statistic_diff(gl_var_1,gl_var_2))
# plt.boxplot([gl_var_1, gl_var_2])
# plt.xticks([1, 2] , [box_1, box_2])

# plt.figure("Minimum Goals")
# plt.title(get_statistic_diff(gl_min_1,gl_min_2))
# plt.boxplot([gl_min_1, gl_min_2])
# plt.xticks([1, 2] , [box_1, box_2])

# plt.figure("Premier quartile Goals")
# plt.title(get_statistic_diff(gl_qa1_1,gl_qa1_2))
# plt.boxplot([gl_qa1_1, gl_qa1_2])
# plt.xticks([1, 2] , [box_1, box_2])

# plt.figure("Mediane Goals")
# plt.title(get_statistic_diff(gl_med_1,gl_med_2))
# plt.boxplot([gl_med_1, gl_med_2])
# plt.xticks([1, 2] , [box_1, box_2])

# plt.figure("Troisième quartile Goals")
# plt.title(get_statistic_diff(gl_qa3_1,gl_qa3_2))
# plt.boxplot([gl_qa3_1, gl_qa3_2])
# plt.xticks([1, 2] , [box_1, box_2])

# plt.figure(["Maximum Goals"])
# plt.title(get_statistic_diff(gl_max_1,gl_max_2))
# plt.boxplot([gl_max_1, gl_max_2])
# plt.xticks([1, 2] , [box_1, box_2])



plt.figure("Moyenne Ikpy")
# plt.title(get_statistic_diff(ik_moy_1,ik_moy_2))
# plt.boxplot([ik_moy_1, ik_moy_2])
# plt.xticks([1, 2] , [box_1, box_2])
plt.title( text.format(
    get_statistic_diff(ik_moy_1,ik_moy_2),
    get_statistic_diff(ik_moy_2,ik_moy_3),
    get_statistic_diff(ik_moy_1,ik_moy_3)
))
plt.boxplot([ik_moy_1, ik_moy_2, ik_moy_3])
plt.xticks([1, 2, 3] , [box_1, box_2, box_3])

# plt.figure("Variance Ikpy")
# plt.title(get_statistic_diff(ik_var_1,ik_var_2))
# plt.boxplot([ik_var_1, ik_var_2])
# plt.xticks([1, 2] , [box_1, box_2])

# plt.figure("Minimum Ikpy")
# plt.title(get_statistic_diff(ik_min_1,ik_min_2))
# plt.boxplot([ik_min_1, ik_min_2])
# plt.xticks([1, 2] , [box_1, box_2])

# plt.figure("Premier quartile Ikpy")
# plt.title(get_statistic_diff(ik_qa1_1,ik_qa1_2))
# plt.boxplot([ik_qa1_1, ik_qa1_2])
# plt.xticks([1, 2] , [box_1, box_2])

# plt.figure("Mediane Ikpy")
# plt.title(get_statistic_diff(ik_med_1,ik_med_2))
# plt.boxplot([ik_med_1, ik_med_2])
# plt.xticks([1, 2] , [box_1, box_2])

# plt.figure("Troisième quartile Ikpy")
# plt.title(get_statistic_diff(ik_qa3_1,ik_qa3_2))
# plt.boxplot([ik_qa3_1, ik_qa3_2])
# plt.xticks([1, 2] , [box_1, box_2])

# plt.figure("Maximum Ikpy")
# plt.title(get_statistic_diff(ik_max_1,ik_max_2))
# plt.boxplot([ik_max_1, ik_max_2])
# plt.xticks([1, 2] , [box_1, box_2])

plt.show()