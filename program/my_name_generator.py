
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