import argparse

def float_01(value):
    fvalue = float(value)
    if fvalue < 0 or fvalue > 1:
        raise argparse.ArgumentTypeError("%s is not a float between 0 and 1" % value)
    return fvalue

def float_1plus(value):
    fvalue = float(value)
    if fvalue < 1:
        raise argparse.ArgumentTypeError("%s is not a float >= 1" % value)
    return fvalue

def pos_int(value):
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError("%s is not a positive int" % value)
    return ivalue

def get_options():
    parser = argparse.ArgumentParser(description='A new way of getting an Inverse Model for a robot with Motor and Goal babling. Robot used : PoppyErgoJr.')

    parser.add_argument("--learning", 
                        dest="learning",
                        action='store_false',
                        default=True,  
                        help="Execute the learning step, default=True"
    )
    parser.add_argument("--file", 
                        dest="use_file",
                        action='store_true',
                        default=False,  
                        help="Enable saving in learning and loading in analyse, default=False"
    )
    parser.add_argument("--n",
                        dest="n",
                        type=str,
                        default="",
                        help="Number (or else) to add at the end of the filename"
    )
    parser.add_argument("--analyse", 
                        dest="analyse",
                        action='store_true',
                        default=False,  
                        help="Execute the analyse step, default=False"
    )
    parser.add_argument("--gg", 
                        dest="gg",
                        type=str,
                        default="frontier",
                        choices=["frontier","agnostic"],
                        help= "Wich goal generator to use in learning process, default=frontier"
    )
    parser.add_argument("--exp", 
                        dest="exp",
                        type=float_1plus,
                        default=1.4,  
                        help= "Expansion coefficient, default=1.4"
    )
    parser.add_argument("--size", 
                        dest="size",
                        type=float,
                        default=0.01,  
                        help= "Cell size for the discretisation (goal on grid), default=0.01"
    )
    parser.add_argument("--p_exp", 
                        dest="p_exp",
                        type=float_01,
                        default=0.5,
                        help= "Probability of exploration, default=0.5"
    )
    parser.add_argument("--steps", 
                        dest="steps",
                        type=pos_int,
                        default=10000,
                        help= "Number of steps for the learning process, default=10 000"
    )
    parser.add_argument("--mb", 
                        dest="mb",
                        type=float_01,
                        default=0.2,  
                        help= "Proportion of motor babling steps in total learning steps, default=0.2"
    )
    parser.add_argument("--pp", 
                        dest="pp",
                        type=float,
                        default=0.01,  
                        help= "Perturbation in degree to randomize a posture, default=0.01"
    )
    

    return parser.parse_args()