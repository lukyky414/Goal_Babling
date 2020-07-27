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

def get_options_goal():
    parser = argparse.ArgumentParser(description='Generate a list of goal to reach for the Inverse Model.')


    parser.add_argument("--seed",
                        dest="seed",
                        type=int,
                        default=None,
                        help="The seed to initiate random numbers. Leave empty for random seed"
    )


    parser.add_argument("--nodebug", 
                        dest="debug",
                        action='store_false',
                        default=True,  
                        help="Do not print debug infos"
    )


    return parser.parse_args()

def get_options_analyse():
    parser = argparse.ArgumentParser(description='Analysing the result of the Inverse Model.')

    parser.add_argument("file",
                        type=str,
                        default=None,
                        help="File generated by `main_inverse_model`."
    )
    parser.add_argument("--size", 
                        dest="size",
                        type=float,
                        default=0.01,  
                        help= "Cell size for the discretisation (goal on grid -> frontier), default=0.01"
    )


    parser.add_argument("--nodebug", 
                        dest="debug",
                        action='store_false',
                        default=True,  
                        help="Do not print debug infos"
    )


    return parser.parse_args()

def get_options_result():
    parser = argparse.ArgumentParser(description='Using the Inverse Model generated by the learning with a generic list of point.')

    parser.add_argument("file",
                        type=str,
                        default=None,
                        help="File generated by `main_learning`. No need to give .dat or .idx"
    )


    parser.add_argument("--nodebug", 
                        dest="debug",
                        action='store_false',
                        default=True,  
                        help="Do not print debug infos"
    )


    return parser.parse_args()

def get_options_learning():
    parser = argparse.ArgumentParser(description='A new way of getting an Inverse Model for a robot with Motor and Goal babling. Robot used : PoppyErgoJr.')


    parser.add_argument("--nodebug", 
                        dest="debug",
                        action='store_false',
                        default=True,  
                        help="Do not print debug infos"
    )

    parser.add_argument("--n",
                        dest="n",
                        type=str,
                        default=None,
                        help="Number (or else) to add at the end of the filename"
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
                        help= "Perturbation in degree to randomize a posture during the learning process, default=0.01"
    )


    parser.add_argument("--gg", 
                        dest="gg",
                        type=str,
                        default=None,
                        choices=["frontier","agnostic"],
                        help= "Wich goal generator to use in learning process, default=None"
    )
    parser.add_argument("--exp", 
                        dest="exp",
                        type=float_1plus,
                        default=1.4,  
                        help= "Expansion coefficient for agnostic goal generator, default=1.4"
    )
    parser.add_argument("--size", 
                        dest="size",
                        type=float,
                        default=0.01,  
                        help= "Cell size for the discretisation (goal on grid -> frontier), default=0.01"
    )
    parser.add_argument("--p_exp", 
                        dest="p_exp",
                        type=float_01,
                        default=0.5,
                        help= "Probability of exploration (goal on grid -> frontier), default=0.5"
    )


    parser.add_argument("--seed",
                        dest="seed",
                        type=int,
                        default=None,
                        help="The seed to initiate random numbers. Leave empty for random seed"
    )
    

    return parser.parse_args()