# Make sure that the program doesn't launch any graphical display or it will wait for the user to quit and make timer wrong.

start_time=`date +%s`;
clear; clear;
python main.py && echo run time is $(expr `date +%s` - $start_time) s
