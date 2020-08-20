
def get_file_name(options):
    """`options` généré avec my_option.get_options_learn()"""

    name = "{}mb-{}gb_{}step".format(options.mb, 1-options.mb, options.step)

    if options.mb != 1:
        name += "_{}pp_{}".format(options.pp, options.gg)

    if options.gg == "agnostic":
        name += "_{}exp".format(options.exp)

    elif options.gg == "frontier":
        name += "_{}pexp-{}res".format(options.p_exp, options.nb_div)

    name += "_{}".format(options.n)

    return name

def get_options(filename):
    name = filename.split("_")
    options = {}

    options["mb"] = float(name[0].split("mb")[0])
    options["step"] = int(name[1][:-4])
    

    if options["mb"] != 1:
        options["pp"] = float(name[2][:-2])
        options["gg"] = name[3]
    
        if options["gg"] == "agnostic":
            options["exp"] = float(name[4][:-3])
        
        if options["gg"] == "frontier":
            options["pexp"] = float(name[4].split("pexp")[0])
            options["res"] = int(name[4].split("-")[1][:-3])
    
    return options


if __name__ == "__main__":
    import my_option

    options = my_option.get_options_learn()

    print(get_file_name(options))