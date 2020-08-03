"""Pour empecher le prompt de pygame, faire "export PYGAME_HIDE_SUPPORT_PROMPT=hide" """

import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
import numpy as np
import pygame as pg

import math
import time
import matplotlib.pyplot as plt
import ctypes

from my_robot import Robot
from my_end_point import EndPoint
from my_discretisation import Discretisation

# print("Left Click - Rotate")
# print("Right Click - Translate")
# print("Wheel Up & Down - Zoom in & out")
# print("CTRL + : zoom in / CTRL - : zoom out")

# Quelques variables constantes pour le programme
# Taille de la fenêtre
_size = (600, 600)
# Couleurs du background [0 - 255] (r, g, b)
_background_color = (0, 0, 0)


def plots_distribution(endpoints : list, precision = 100):
    """Cree quatre plots, un pour chacun des axes et un pour la distance à l'origine, et affiche la distribution des points sur ces graphes
    `endoints` - Liste des endpoints etudiés
    `precision` - Nombre de division de l'espace pour chaques graphes"""

    #Les différents tableaux contenant les données des axes
    xs = [0] * precision
    ys = [0] * precision
    zs = [0] * precision
    ds = [0] * precision
    
    #Pour retenir les minimum et maximum
    mi_x = endpoints[0].get_pos()[0]
    ma_x = endpoints[0].get_pos()[0]
    mi_y = endpoints[1].get_pos()[1]
    ma_y = endpoints[1].get_pos()[1]
    mi_z = endpoints[2].get_pos()[2]
    ma_z = endpoints[2].get_pos()[2]
    ma_d = dist((0, 0, 0), endpoints[0].get_pos())

    nb = len(endpoints)
    
    #Calcul des minimums et maximum
    for ep in endpoints:
        pos = ep.get_pos()
        d = dist((0, 0, 0), pos)

        if pos[0] < mi_x:
            mi_x = pos[0]
        if pos[0] > ma_x:
            ma_x = pos[0]

        if pos[1] < mi_y:
            mi_y = pos[1]
        if pos[1] > ma_y:
            ma_y = pos[1]

        if pos[2] < mi_z:
            mi_z = pos[2]
        if pos[2] > ma_z:
            ma_z = pos[2]
        
        if d > ma_d:
            ma_d = d

    # Le pas pour chacun des axes est calculé avec la précision
    step_x = (ma_x-mi_x)/precision
    step_y = (ma_y-mi_y)/precision
    step_z = (ma_z-mi_z)/precision
    step_d = (ma_d)/precision

    # Maintenant que les bornes sont connues, calcul des valeurs à afficher
    for ep in endpoints:
        x, y, z = ep.get_pos()
        d = dist((0, 0, 0), (x, y, z))

        x_index = math.floor(precision*(x-mi_x)/(ma_x-mi_x))
        y_index = math.floor(precision*(y-mi_y)/(ma_y-mi_y))
        z_index = math.floor(precision*(z-mi_z)/(ma_z-mi_z))
        d_index = math.floor(precision*(   d  )/(   ma_d  ))

        if x_index == precision:
            x_index -= 1
        if y_index == precision:
            y_index -= 1
        if z_index == precision:
            z_index -= 1
        if d_index == precision:
            d_index -= 1
        
        xs[x_index] += 1
        ys[y_index] += 1
        zs[z_index] += 1
        ds[d_index] += 1

    # Calcul des index a afficher sur chacun des axes
    axe_x = []
    axe_y = []
    axe_z = []
    axe_d = []
    for i in range(precision):
        axe_x.append(i * step_x + mi_x)
        axe_y.append(i * step_y + mi_y)
        axe_z.append(i * step_z + mi_z)
        axe_d.append(i * step_d       )
        

    # Affichage sur plusieurs fenêtres (grâce à plt.figure())
    plt.plot(axe_x, xs)
    plt.ylabel("Number of points")
    plt.xlabel("X coordinates")

    plt.figure()
    plt.plot(axe_y, ys)
    plt.ylabel("Number of points")
    plt.xlabel("Y coordinates")

    plt.figure()
    plt.plot(axe_z, zs)
    plt.ylabel("Number of points")
    plt.xlabel("Z coordinates")

    plt.figure()
    plt.plot(axe_d, ds)
    plt.ylabel("Number of points")
    plt.xlabel("Distance from origin")

    plt.show()

def draw_discretization(grid : Discretisation, alpha_per_point = 0.01, d=None):
    """Permet de représenter le tableau de la discretisation de l'espace. Chaque case est transparente, mais l'est de moins en moins en fonction du nombre de points dans celle-ci. Réglable avec `alpha_per_point`
    `d` si préciser représente une sphère. (vecteur directeur)"""

    _init_display()

    size = grid.size
    mins = grid.min


    while _StaticVars.is_running:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)

        _draw_axes()

        for cell in grid.visited:
            x = cell[0] * size + mins[0]
            y = cell[1] * size + mins[1]
            z = cell[2] * size + mins[2]

            a = grid.get_cell(cell) * alpha_per_point
            if a > 1:
                a = 1

            gl.glColor4f(0, 1, 0, a)

            _draw_cube((x,y,z),size)
        
        #Permet d'afficher une direction pour tester l'algo frontier
        if d is not None:
            gl.glColor3f(1, 0, 0)
            gl.glPushMatrix()
            gl.glTranslatef(d[0], d[1], d[2])
            glu.gluSphere(glu.gluNewQuadric(), 0.03, 16, 16)
            gl.glPopMatrix()


        _draw_fps()
        pg.display.flip()
        _event_handler()
        pg.time.wait(10)

def animation(robot : Robot):
    """Creer une animation avec le robot, en faisant tourner un à un les moteurs dans les limites de ceux-ci"""
    global _background_color
    _background_color = (255, 255, 255)
    _init_display()

    angles = [0 for _ in range(robot.nb_joints)]
    limits = robot.get_angle_bounds()

    angle = limits[0][0]
    sense = limits[0][0] < limits[0][1]
    new_angle = False

    i = 0

    while _StaticVars.is_running:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)
        _draw_axes()

        if sense:
            angle = angle + 0.5
            if angle > limits[i][1]:
                new_angle = True
        else:
            angle = angle - 0.5
            if angle < limits[i][1]:
                new_angle = True

        if new_angle:
            angles[i] = 0
            i = (i+1) % robot.nb_joints
            angle = limits[i][0]
            sense = limits[i][0] < limits[i][1]
            new_angle = False

        angles[i] = angle

        posture = robot.get_posture_pos(angles=angles)

        print("{} : {}     ".format(i, angle), end='\r')
        _draw_one_robot(posture_pos=posture, highlight=i)

        _draw_fps()
        pg.display.flip()
        _event_handler()
        pg.time.wait(10)

def display_robot(posture_pos : list):
    """Dessine un ou plusieurs robot.
    `posture_pos` - Liste de matrice de rotation pour chacun des points du robot. Une liste de liste affichera plusieurs robots"""

    _init_display()

    while _StaticVars.is_running:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)

        _draw_axes()

        if isinstance(posture[0], list):
            for r in posture:
                _draw_one_robot(posture=r)
        else:
            _draw_one_robot(posture=posture)

        _draw_fps()
        pg.display.flip()
        _event_handler()
        pg.time.wait(10)

def draw_points_cloud(end_points : list, max_dist = 0.3):
    """Dessine un nuage de point 3d.
    `end_points` - les coordonnees des points en (x, y, z) ou liste d'end_points"""

    _init_display()

    # Calcul de la couleur des points avant affichage
    points = []
    for ep in end_points:
        if isinstance(ep, EndPoint):
            pos = ep.get_pos()
        else:
            pos = ep
        d = 0
        for p in pos:
            d += p**2
        d = math.sqrt(d)

        fact = d / max_dist
        color = _get_rainbow_color(fact)
        points.append((pos, color))

    while _StaticVars.is_running:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)

        _draw_axes()

        gl.glBegin(gl.GL_POINTS)
        for p in points:
            gl.glColor3f(p[1][0], p[1][1], p[1][2])

            gl.glVertex3f(p[0][0], p[0][1], p[0][2])

        gl.glEnd()

        _draw_fps()
        pg.display.flip()
        _event_handler()
        pg.time.wait(10)

def draw_ep_and_goal(end_points : list, goals : list):
    """Dessine un nuage de point 3d.
    `end_points` - les end_points
    `goals` - les goals"""

    _init_display()

    while _StaticVars.is_running:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)

        _draw_axes()

        gl.glBegin(gl.GL_POINTS)

        #Rouge pour les goals
        for g in goals:
            gl.glColor3f(1, 0, 0)
            (x, y, z) = g
            gl.glVertex3f(x, y, z)

        #Bleu pour les endpoints
        for ep in end_points:
            gl.glColor3f(0, 0, 1)
            (x, y, z) = ep.get_pos()
            gl.glVertex3f(x, y, z)

        gl.glEnd()

        _draw_fps()
        pg.display.flip()
        _event_handler()
        pg.time.wait(10)

def _init_display():
    """Initialise l'affichage."""
    glut.glutInit()
    pg.init()
    pg.display.set_mode(_size, pg.OPENGL)

    # Perspective de vue du modele: fov, ratio, near & far clipping plane
    glu.gluPerspective(45, (_size[0]/_size[1]), 0.1, 50.0)

    # Reculer le point de vue pour voir la scene
    gl.glTranslatef(0.0, 0.0, -3)

    # De base, Z est un axe de profondeur (il viens vers la camera) et Y est vertical.
    gl.glRotatef(-90, 1, 0, 0) # Mettre Z vers le haut, mais du coup Y est "loin"
    gl.glRotatef(180, 0, 0, 1) # Mettre Y vers la camera

    # Avoir le X (rouge) qui part a droite
    gl.glScalef(-1, 1, 1)

    # Pour garder cet etat de base
    gl.glPushMatrix()

    # Couleur de fond
    gl.glClearColor(_background_color[0]/255, _background_color[1]/255, _background_color[2]/255, 1.0)

    #Autoriser la transparence
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    #Orientation des faces
    gl.glEnable(gl.GL_CULL_FACE)
    gl.glEnable(gl.GL_DEPTH_TEST)

    #Initialisation des variables statiques
    _StaticVars.is_running = True
    _StaticVars.mouse_left_pressed = False
    _StaticVars.mouse_right_pressed = False
    _StaticVars.keyboard_ctrl_pressed = False
    _StaticVars.mouse_last_x = 0
    _StaticVars.mouse_last_y = 0
    _StaticVars.last_time = 0

class _StaticVars:
    #Variables statiques pour l'execution du programme
    is_running = True
    mouse_left_pressed = False
    mouse_right_pressed = False
    keyboard_ctrl_pressed = False
    mouse_last_x = 0
    mouse_last_y = 0
    last_time = 0

def _draw_one_robot(posture_pos : list, highlight=None):
    """Permet de dessiner un robot avec ces link et ses moteurs.
    `posture_pos` - liste de matrice de rotation décrivant le robot dans sa posture"""

    # Chaque section est representee par un segment noir
    gl.glBegin(gl.GL_LINE_STRIP)
    gl.glColor3ui(0, 0, 0)

    for section in posture_pos:
        gl.glVertex3f(section[0][3], section[1][3], section[2][3])

    gl.glEnd()


    # Chaque moteur est represente par une sphere bleue
    for i in range(len(posture_pos)):
        # Si on veux mettre en valeur un moteur, on l'affiche en rouge (pour l'animation)
        if highlight is not None and i == highlight+1:
            gl.glColor3ui(255, 0, 0)
        else:
            gl.glColor3ui(0, 0, 255)
        gl.glPushMatrix()
        gl.glTranslatef(posture_pos[i][0][3], posture_pos[i][1][3], posture_pos[i][2][3])
        glu.gluSphere(glu.gluNewQuadric(), 0.003, 16, 16)
        gl.glPopMatrix()

def _draw_cube(pos : tuple, size : float):
    """Dessine un cube à la position `pos` et de taille `size`"""
    #Le cube se tient dans x, y, z et x+size, y+size, z+size
    x = pos[0]
    y = pos[1]
    z = pos[2]

    # Il n'existe pas de GL_QUAD, toutes les faces sont séparées en triangles
    # Orientation importante
    gl.glBegin(gl.GL_TRIANGLES)
    gl.glVertex3f(x, y, z)
    gl.glVertex3f(x+size, y, z)
    gl.glVertex3f(x+size, y, z+size)

    gl.glVertex3f(x, y, z)
    gl.glVertex3f(x+size, y, z+size)
    gl.glVertex3f(x, y, z+size)

    gl.glVertex3f(x+size, y, z)
    gl.glVertex3f(x+size, y+size, z)
    gl.glVertex3f(x+size, y+size, z+size)

    gl.glVertex3f(x+size, y, z)
    gl.glVertex3f(x+size, y+size, z+size)
    gl.glVertex3f(x+size, y, z+size)

    gl.glVertex3f(x+size, y+size, z)
    gl.glVertex3f(x, y+size, z)
    gl.glVertex3f(x, y+size, z+size)

    gl.glVertex3f(x+size, y+size, z)
    gl.glVertex3f(x, y+size, z+size)
    gl.glVertex3f(x+size, y+size, z+size)

    gl.glVertex3f(x, y+size, z)
    gl.glVertex3f(x, y, z)
    gl.glVertex3f(x, y, z+size)

    gl.glVertex3f(x, y+size, z)
    gl.glVertex3f(x, y, z+size)
    gl.glVertex3f(x, y+size, z+size)

    gl.glVertex3f(x, y, z+size)
    gl.glVertex3f(x+size, y, z+size)
    gl.glVertex3f(x+size, y+size, z+size)

    gl.glVertex3f(x, y, z+size)
    gl.glVertex3f(x+size, y+size, z+size)
    gl.glVertex3f(x, y+size, z+size)

    gl.glVertex3f(x, y, z)
    gl.glVertex3f(x, y+size, z)
    gl.glVertex3f(x+size, y+size, z)

    gl.glVertex3f(x, y, z)
    gl.glVertex3f(x+size, y+size, z)
    gl.glVertex3f(x+size, y, z)
    gl.glEnd()

def _draw_axes():
    """Dessine les différents axes. X - Rouge, Y - Bleu, Z - Vert"""

    #Côté positif, ligne pleine
    gl.glBegin(gl.GL_LINES)
    # X
    gl.glColor3f(1, 0, 0)
    gl.glVertex3f(0, 0, 0)
    gl.glVertex3f(1, 0, 0)
    # Y
    gl.glColor3f(0, 0, 1)
    gl.glVertex3f(0, 0, 0)
    gl.glVertex3f(0, 1, 0)
    # Z
    gl.glColor3f(0, 1, 0)
    gl.glVertex3f(0, 0, 0)
    gl.glVertex3f(0, 0, 1)
    gl.glEnd()

    #Côté négatif, ligne en pointillé
    gl.glPushAttrib(gl.GL_ENABLE_BIT)
    # Pointilles
    gl.glLineStipple(1, 0xa0a0)
    gl.glEnable(gl.GL_LINE_STIPPLE)
    gl.glBegin(gl.GL_LINES)
    # -X
    gl.glColor3f(1, 0, 0)
    gl.glVertex3f(0, 0, 0)
    gl.glVertex3f(-1, 0, 0)
    # -Y
    gl.glColor3f(0, 0, 1)
    gl.glVertex3f(0, 0, 0)
    gl.glVertex3f(0, -1, 0)
    #-Z
    gl.glColor3f(0, 1, 0)
    gl.glVertex3f(0, 0, 0)
    gl.glVertex3f(0, 0, -1)
    gl.glEnd()
    gl.glPopAttrib()

def _draw_fps():
    """Dessine les fps à l'écran"""
    gl.glColor3ui(0, 255, 0)

    t = time.time()
    elapsed = t - _StaticVars.last_time
    fps = str(math.floor(1 / elapsed))
    _StaticVars.last_time = t
    
    gl.glPushMatrix()
    gl.glLoadIdentity()
    gl.glRasterPos2f(-1, 0.9)
    for ch in fps:
        glut.glutBitmapCharacter( glut.GLUT_BITMAP_8_BY_13 , ctypes.c_int( ord(ch) ) )
    gl.glPopMatrix()

def _get_rainbow_color(fact : float):
    """Retourne une couleur de l'arc en ciel avec un facteur."""
    # avoir une valeur entre 0 et 1.
    fact = fact - math.floor(fact)
    
    if fact < 1/3:
        return (1-(fact*3), fact*3, 0)
    elif fact < 2/3:
        return (0, 2-fact*3, fact*3-1)
    else:
        return (fact*3-2, 0, 3-fact*3)


#Variable contante pour éviter de recréer / calculer à chaque fois
_x_axe = np.array(( (1, 0, 0, 0),
                    (0, 1, 0, 0),
                    (0, 0, 1, 0),
                    (1, 0, 0, 1)))
_y_axe = np.array(( (1, 0, 0, 0),
                    (0, 1, 0, 0),
                    (0, 0, 1, 0),
                    (0, 1, 0, 1)))
_z_axe = np.array(( (1, 0, 0, 0),
                    (0, 1, 0, 0),
                    (0, 0, 1, 0),
                    (0, 0, 1, 1)))

def _event_handler():
    """Prend en charge les evenements pygame"""
    _mouse_handler()
    for event in pg.event.get():
        _mouse_event(event)
        _closing_event(event)
        _keyboard_event(event)

def _keyboard_event(event):
    """Trie les event pour prendre en compte les touches du clavier utilisée"""
    #Relachement d'une touche
    if event.type == pg.KEYUP:
        #Relachement de la touche controle
        if event.key == pg.K_LCTRL or event.key == pg.K_RCTRL:
            _StaticVars.keyboard_ctrl_pressed = False
    #Appui d'une touche
    elif event.type == pg.KEYDOWN:
        #Appui sur une touche controle (droite ou gauche)
        if event.key == pg.K_LCTRL or event.key == pg.K_RCTRL:
            _StaticVars.keyboard_ctrl_pressed = True

        #Appui sur une fleche: recentrer la vue sur un axe

        #up = cacher axe Z (vert)
        elif event.key == pg.K_UP:
            gl.glPopMatrix()
            gl.glPushMatrix()
            gl.glRotatef(90, 1, 0, 0)
        #down = cacher axe y (bleu)
        elif event.key == pg.K_DOWN:
            gl.glPopMatrix()
            gl.glPushMatrix()
        #right = cacher axe x (rouge)
        elif event.key == pg.K_RIGHT:
            gl.glPopMatrix()
            gl.glPushMatrix()
            gl.glRotatef(-90, 0, 0, 1)


        #Si controle est appuyé, verification du + et -
        if _StaticVars.keyboard_ctrl_pressed:
            if event.key == pg.K_PLUS or event.key == pg.K_KP_PLUS:
                gl.glScalef(1.5, 1.5, 1.5)
            elif event.key == pg.K_MINUS or event.key == pg.K_KP_MINUS:
                gl.glScalef(0.6, 0.6, 0.6)

def _closing_event(event):
    """Toutes les manières de quitter l'appli"""
    #La ptite croix, alt+f4, etc... et enfin la touche échape
    if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
        pg.quit()
        _StaticVars.is_running = False
        print()

def _mouse_event(event):
    """Enregistre les informations de la souris"""
    #N'a aucun effet directe sur l'affichage. Tout sera fait dans _mouse_handler
    if event.type == pg.MOUSEBUTTONDOWN:
        # Left Click
        if event.button == 1:
            _StaticVars.mouse_left_pressed = True
            _StaticVars.mouse_last_x, _StaticVars.mouse_last_y = pg.mouse.get_pos()

        elif event.button == 3:
            _StaticVars.mouse_right_pressed = True
            _StaticVars.mouse_last_x, _StaticVars.mouse_last_y = pg.mouse.get_pos()

        # Wheel Up = Zoom
        elif event.button == 4:
            gl.glScalef(1.5, 1.5, 1.5)

        # Wheel Down = Dezoom
        elif event.button == 5:
            gl.glScalef(0.6, 0.6, 0.6)

    elif event.type == pg.MOUSEBUTTONUP:
        if event.button == 1:
            _StaticVars.mouse_left_pressed = False

        elif event.button == 3:
            _StaticVars.mouse_right_pressed = False


# Rapport entre le déplacement de la souris et la translation du monde
_translation_factor = 1/120

def _mouse_handler():
    if _StaticVars.mouse_left_pressed or _StaticVars.mouse_right_pressed:# Position actuelle de la souris
        curr_x, curr_y = pg.mouse.get_pos()

        # Deplacement relatif a la derniere position
        depl_x, depl_y = curr_x-_StaticVars.mouse_last_x, curr_y-_StaticVars.mouse_last_y

        # Recuperer la matrice du modelview inverse
        matrix = np.linalg.inv(gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX))
        # Ignorer les facteurs de zoom
        matrix[3] = (0, 0, 0, 1)

        # Recuperer l'orientation des axes x et y
        curr_y_axes = _y_axe.dot(matrix)
        curr_x_axes = _x_axe.dot(matrix)

        # Mise a jour de la derniere position
        _StaticVars.mouse_last_x = curr_x
        _StaticVars.mouse_last_y = curr_y

        if _StaticVars.mouse_right_pressed:
            # Effectuer une translation sur le repère de la caméra.
            # Un déplacement vertical doit être inversé.
            gl.glTranslatef(curr_x_axes[3][0]*(depl_x*_translation_factor), curr_x_axes[3][1]*(depl_x*_translation_factor), curr_x_axes[3][2]*(depl_x*_translation_factor))
            gl.glTranslatef(curr_y_axes[3][0]*(-depl_y*_translation_factor), curr_y_axes[3][1]*(-depl_y*_translation_factor), curr_y_axes[3][2]*(-depl_y*_translation_factor))


        elif _StaticVars.mouse_left_pressed:
            # Effectuer une rotation autour de ces axes (et non autour de l'axe monde).
            # Deplacer la souris horizontalement (x) fait tourner le monde sur l'axe vertical (y) et vice-versa.
            gl.glRotatef(-depl_x, curr_y_axes[3][0], curr_y_axes[3][1], curr_y_axes[3][2])
            gl.glRotatef(-depl_y, curr_x_axes[3][0], curr_x_axes[3][1], curr_x_axes[3][2])
