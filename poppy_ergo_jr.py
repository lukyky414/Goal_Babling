from Robots import Arm3D, Articulation3D


def get_robot():
    my_poppy = Arm3D(articulations=[
        Articulation3D(
            origin=(
                (0, 0, 0.0327993216120967),
                (-6.12303176911189e-17, 0, 0)
            ),
            axe=(0, 0, -1),
            angle_min=-150,
            angle_max=150
        ),
        Articulation3D(
            origin=(
                (0, 0, 0.0240006783879033),
                (1.5707963267949, 0, 0)
            ),
            axe=(-1, 0, 0),
            angle_min=-90,
            angle_max=125
        ),
        Articulation3D(
            origin=(
                (0, 0.054, 0),
                (0, 0, 0)
            ),
            axe=(-1, 0, 0),
            angle_min=-90,
            angle_max=90
        ),
        Articulation3D(
            origin=(
                (0, 0.0298217741221248, 0),
                (3.141592653589, 0, 0)
            ),
            axe=(0, 1, 0),
            angle_min=-150,
            angle_max=150
        ),
        Articulation3D(
            origin=(
                (0, -0.0151782258778753, -0.048),
                (-1.5707963267949, 0, 0)
            ),
            axe=(-1, 0, 0),
            angle_min=-90,
            angle_max=90
        ),
        Articulation3D(
            origin=(
                (0, 0.054, 0),
                (1.5707963267949, 1.5707963267949, 0)
            ),
            axe=(0, -1, 0),
            angle_min=-110,
            angle_max=90
        )
    ])


    my_poppy.execute([
        -120,
        125,
        -45,
        0,
        45,
        45
    ])

    return my_poppy
