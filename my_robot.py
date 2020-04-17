from ikpy.chain import Chain
import sys
import random

def get_position(robot: Chain, angles: list):
    """Retourne la position du `end_point` du `robot` en executant les `angles` donnes"""

    # Le premier `link` du robot est inutile. Il sert juste de base et une rotation ne change rien au reste.
    if len(angles) != len(robot.links)-1:
        print("Nombre d'angle {} ne correspond pas a la taille du robot {}".format(len(angles), len(robot.links)-1), file=sys.stderr)
        exit(1)
    
    new_angles = angles.copy()
    new_angles.insert(0, 0.0)

    matrix = robot.forward_kinematics(joints=new_angles)

    return (matrix[0][3], matrix[1][3], matrix[2][3])

def get_posture(robot: Chain, angles: list):
    """Retourne la posture (position de chacune des sections) du `robot` en executant les `angles` donnes"""

    # Le premier `link` du robot est inutile. Il sert juste de base et une rotation ne change rien au reste.
    if len(angles) != len(robot.links)-1:
        print("Nombre d'angle {} ne correspond pas a la taille du robot {}".format(len(angles), len(robot.links)-1), file=sys.stderr)
        exit(1)

    new_angles = angles.copy()
    new_angles.insert(0, 0.0)

    matrixes = robot.forward_kinematics(joints=new_angles, full_kinematics=True)

    res = []

    for m in matrixes:
        res.append((m[0][3], m[1][3], m[2][3]))

    return res

def get_random_posture_angles(robot: Chain):
    """Retourne une liste d'angle aleatoire executable par le `robot`"""

    res = []

    for motor in robot.links:
        if motor.bounds[0] is not None:
            res.append(random.uniform(motor.bounds[0], motor.bounds[1]))

    return res

def randomize_posture(robot: Chain, angles: list):
    """Change aleatoirement la posture du robot dans les limites des moteurs"""

    # Perturbation de 15 deg
    disturb = 0.2617993878

    res = []

    links = robot.links.copy()
    links.pop(0)

    for motor, angle in zip(links, angles):
        res.append(
            random.uniform(
                max(
                    motor.bounds[0], (angle - disturb)
                ),
                min(
                    motor.bounds[1], (angle + disturb)
                )
            )
        )
    
    return res