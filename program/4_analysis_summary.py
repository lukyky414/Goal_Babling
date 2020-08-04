import re
import os
import sys
import glob
import json

from my_files_paths import *
import my_option


options = my_option.get_options_summary()

f = options.file

name = f[f.rfind("/")+1:]
if name[-5:] == ".json":
    name = name[:-5]
end_nb = re.compile("_[\d]+")
if end_nb.match(name[name.rfind("_"):]):
    name = name[:name.rfind("_")]


if len(glob.glob("{}/{}/{}_*.json".format(MAIN_DIR, ANL_DIR, name))) == 0:
    print("No analysis file found for '{}'".format(name), file=sys.stderr)
    sys.exit(1)

files = glob.glob("{}/{}/{}_*.json".format(MAIN_DIR, ANL_DIR, name))

RESULTS = {}


for f in files:
    s = open(f, "r")
    res = json.load(fp=s)

    for ind in res:
        if not RESULTS.__contains__(ind):
            RESULTS[ind] = []
        RESULTS[ind].append(res[ind])

print(RESULTS)