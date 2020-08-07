import os

from my_files_paths import *

def create(path):
    if not os.path.exists(path):
        os.makedirs(path)

create(MAIN_DIR)
create("{}/{}".format(MAIN_DIR, CTL_DIR))

for algo in ["motor_babling", "agnostic", "frontier"]:
    create("{}/{}/{}".format(MAIN_DIR, CTL_DIR, algo))