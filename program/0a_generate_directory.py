import os

from my_files_paths import *

os.makedirs(MAIN_DIR)
os.makedirs("{}/{}".format(MAIN_DIR, CTL_DIR))