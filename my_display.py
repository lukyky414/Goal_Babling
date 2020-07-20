"""Pour empecher le prompt de pygame, faire "export PYGAME_HIDE_SUPPORT_PROMPT=hide" """

import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
import numpy as np
import pygame as pg
from math import pi, sqrt
from my_robot import Robot
from my_end_point import EndPoint
from my_discretisation import Discretisation
from my_analyse import difference_discretisation
import math
import time
import ctypes

# Quelques variables constantes pour le programme
_PRINT_HELP_ = False
_translation_factor = 1/120
_size = (600, 600)
_background_color = (0, 0, 0)
_font_color = (0, 255, 0)
_point_color = (0, 0, 255)
_highlight_color = (255, 0, 0)
_joint_color = (0, 0, 0)
_x_axe = np.array(( (1, 0, 0, 0),
                    (0, 1, 0, 0),
                    (0, 0, 1, 0),
                    (1, 0, 0, 1)))
_y_axe = np.array(( (1, 0, 0, 0),
                    (0, 1, 0, 0),
                    (0, 0, 1, 0),
                    (0, 1, 0, 1)))

if _PRINT_HELP_:
    print("Left Click - Rotate")
    print("Right Click - Translate")
    print("Wheel Up & Down - Zoom in & out")
    print("CTRL + : zoom in / CTRL - : zoom out")

def _draw_cube(pos : tuple, size : tuple):
    x = pos[0]
    y = pos[1]
    z = pos[2]

    gl.glBegin(gl.GL_TRIANGLES)
    gl.glVertex3f(x, y, z)
    gl.glVertex3f(x+size[0], y, z)
    gl.glVertex3f(x+size[0], y, z+size[2])

    gl.glVertex3f(x, y, z)
    gl.glVertex3f(x+size[0], y, z+size[2])
    gl.glVertex3f(x, y, z+size[2])

    gl.glVertex3f(x+size[0], y, z)
    gl.glVertex3f(x+size[0], y+size[1], z)
    gl.glVertex3f(x+size[0], y+size[1], z+size[2])

    gl.glVertex3f(x+size[0], y, z)
    gl.glVertex3f(x+size[0], y+size[1], z+size[2])
    gl.glVertex3f(x+size[0], y, z+size[2])

    gl.glVertex3f(x+size[0], y+size[1], z)
    gl.glVertex3f(x, y+size[1], z)
    gl.glVertex3f(x, y+size[1], z+size[2])

    gl.glVertex3f(x+size[0], y+size[1], z)
    gl.glVertex3f(x, y+size[1], z+size[2])
    gl.glVertex3f(x+size[0], y+size[1], z+size[2])

    gl.glVertex3f(x, y+size[1], z)
    gl.glVertex3f(x, y, z)
    gl.glVertex3f(x, y, z+size[2])

    gl.glVertex3f(x, y+size[1], z)
    gl.glVertex3f(x, y, z+size[2])
    gl.glVertex3f(x, y+size[1], z+size[2])

    gl.glVertex3f(x, y, z+size[2])
    gl.glVertex3f(x+size[0], y, z+size[2])
    gl.glVertex3f(x+size[0], y+size[1], z+size[2])

    gl.glVertex3f(x, y, z+size[2])
    gl.glVertex3f(x+size[0], y+size[1], z+size[2])
    gl.glVertex3f(x, y+size[1], z+size[2])

    gl.glVertex3f(x, y, z)
    gl.glVertex3f(x, y+size[1], z)
    gl.glVertex3f(x+size[0], y+size[1], z)

    gl.glVertex3f(x, y, z)
    gl.glVertex3f(x+size[0], y+size[1], z)
    gl.glVertex3f(x+size[0], y, z)
    gl.glEnd()

def draw_diff(grid1 : Discretisation, grid2 : Discretisation, alpha_per_point = 0.1):
    """Permet de représenter le tableau de la discretisation de l'espace. Chaque case est transparente, mais l'est de moins en moins en fonction du nombre de points dans celle-ci. Réglable avec `alpha_per_point`"""

    _init_display()

    size = grid1.size
    min = grid1.min

    #Cellule peuplée par grid1 mais non grid2
    diff1 = difference_discretisation(grid1=grid1, grid2=grid2)
    diff2 = difference_discretisation(grid1=grid2, grid2=grid1)

    while _StaticVars.is_running:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)

        _draw_axes()

        gl.glColor4f(0, 0, 1, 0.3)
        for cell in diff1:
            x = cell[0] * size[0] + min[0]
            y = cell[1] * size[1] + min[1]
            z = cell[2] * size[2] + min[2]

            # a = grid1.get_cell(cell) * alpha_per_point
            # if a > 1:
            #     a = 1
            
            # d = sqrt(x**2 + y**2 + z**2) / 0.3
            # color = _get_rainbow_color(d)

            # gl.glColor4f(color[0], color[1], color[2], a)

            _draw_cube((x,y,z),size)

        gl.glColor4f(1, 0, 0, 0.3)
        for cell in diff2:
            x = cell[0] * size[0] + min[0]
            y = cell[1] * size[1] + min[1]
            z = cell[2] * size[2] + min[2]

            # a = grid2.get_cell(cell) * alpha_per_point
            # if a > 1:
            #     a = 1
            
            # d = sqrt(x**2 + y**2 + z**2) / 0.3
            # color = _get_rainbow_color(d)

            # gl.glColor4f(color[0], color[1], color[2], a)

            _draw_cube((x,y,z),size)

        _draw_fps()
        pg.display.flip()
        _event_handler()
        pg.time.wait(10)

def draw_discretization(grid : Discretisation, alpha_per_point = 0.01):
    """Permet de représenter le tableau de la discretisation de l'espace. Chaque case est transparente, mais l'est de moins en moins en fonction du nombre de points dans celle-ci. Réglable avec `alpha_per_point`"""

    _init_display()

    size = grid.size
    min = grid.min


    while _StaticVars.is_running:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)

        _draw_axes()

        for cell in grid.visited:
            x = cell[0] * size[0] + min[0]
            y = cell[1] * size[1] + min[1]
            z = cell[2] * size[2] + min[2]

            a = grid.get_cell(cell) * alpha_per_point
            if a > 1:
                a = 1

            gl.glColor4f(0, 1, 0, a)

            _draw_cube((x,y,z),size)


        _draw_fps()
        pg.display.flip()
        _event_handler()
        pg.time.wait(10)

def animation(robot : Robot):
    """Creer une animation avec le robot, en faisant tourner un a un les moteurs dans les limites de ceux-ci"""
    
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

        posture = robot.get_posture(angles=angles)

        print("{} : {}     ".format(i, angle), end='\r')
        _draw_one_robot(posture=posture, highlight=i)

        _draw_fps()
        pg.display.flip()
        _event_handler()
        pg.time.wait(10)

def display_robot(posture : list):
    """Dessine plusieurs bras robot 3d.
    `posture` - Liste de points 3D definissant la posture du robot. Une liste de liste affichera plusieurs robots"""

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

def _draw_one_robot(posture : list, highlight=None):
    # Chaque section est representee par un segment
    gl.glBegin(gl.GL_LINE_STRIP)
    gl.glColor3ui(_joint_color[0], _joint_color[1], _joint_color[2])

    for section in posture:
        gl.glVertex3f(section[0][3], section[1][3], section[2][3])

    gl.glEnd()


    # Chaque moteur est represente par une sphere
    for i in range(len(posture)):
        # Si on veux mettre en valeur un joint
        if highlight is not None and i == highlight+1:
            gl.glColor3ui(_highlight_color[0], _highlight_color[1], _highlight_color[2])
        else:
            gl.glColor3ui(_point_color[0], _point_color[1], _point_color[2])
        gl.glPushMatrix()
        gl.glTranslatef(posture[i][0][3], posture[i][1][3], posture[i][2][3])
        glu.gluSphere(glu.gluNewQuadric(), 0.003, 16, 16)
        gl.glPopMatrix()

def _get_rainbow_color(fact : float):
    """Retourne une couleur de l'arc en ciel avec un facteur."""
    # avoir une valeur entre 0 et 1
    fact = fact - math.floor(fact)
    
    if fact < 1/3:
        return (1-(fact*3), fact*3, 0)
    elif fact < 2/3:
        return (0, 2-fact*3, fact*3-1)
    else:
        return (fact*3-2, 0, 3-fact*3)

def draw_points_cloud(end_points : list, max_dist = 0.3):
    """Dessine un nuage de point 3d.
    `points` - les coordonnees des points en (x, y, z)"""

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
        d = sqrt(d)

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

def _draw_axes():
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
    gl.glColor3f(_font_color[0]/255, _font_color[1]/255, _font_color[2]/255)

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

class _StaticVars:
    is_running = True
    mouse_left_pressed = False
    mouse_right_pressed = False
    keyboard_ctrl_pressed = False
    mouse_last_x = 0
    mouse_last_y = 0
    last_time = 0

def _init_display():
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

    # Couleur de fond
    gl.glClearColor(_background_color[0]/255, _background_color[1]/255, _background_color[2]/255, 1.0)

    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    gl.glEnable(gl.GL_CULL_FACE)
    gl.glEnable(gl.GL_DEPTH_TEST)

    
    _StaticVars.is_running = True
    _StaticVars.mouse_left_pressed = False
    _StaticVars.mouse_right_pressed = False
    _StaticVars.keyboard_ctrl_pressed = False
    _StaticVars.mouse_last_x = 0
    _StaticVars.mouse_last_y = 0
    _StaticVars.last_time = 0

def _event_handler():
    _mouse_handler()
    for event in pg.event.get():
        _mouse_event(event)
        _closing_event(event)
        _keyboard_event(event)

def _keyboard_event(event):
    if event.type == pg.KEYUP:
        if event.key == pg.K_LCTRL or event.key == pg.K_RCTRL:
            _StaticVars.keyboard_ctrl_pressed = False
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_LCTRL or event.key == pg.K_RCTRL:
            _StaticVars.keyboard_ctrl_pressed = True
        elif _StaticVars.keyboard_ctrl_pressed:
            if event.key == pg.K_PLUS or event.key == pg.K_KP_PLUS:
                gl.glScalef(1.5, 1.5, 1.5)
            elif event.key == pg.K_MINUS or event.key == pg.K_KP_MINUS:
                gl.glScalef(0.6, 0.6, 0.6)

def _closing_event(event):
    if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
        pg.quit()
        _StaticVars.is_running = False
        print()

def _mouse_event(event):
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
