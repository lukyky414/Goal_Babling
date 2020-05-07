from __future__ import print_function
"""Pour empecher le prompt de pygame, faire "export PYGAME_HIDE_SUPPORT_PROMPT=hide" """

import OpenGL.GL as gl
import OpenGL.GLU as glu
import numpy as np
import pygame as pg
import my_robot
from math import pi

_PRINT_HELP_ = False

if _PRINT_HELP_:
    print("Left Click - Rotate")
    print("Right Click - Translate")
    print("Wheel Up & Down - Zoom in & out")

def animation(robot : my_robot.Robot):
    """Creer une animation avec le robot, en faisant tourner un a un les moteurs dans les limites de ceux-ci"""
    
    _init_display(size=(600,600), background_color=(1, 1, 1), z_up = True)

    angles = [0 for _ in range(robot.get_joint_number())]
    limits = robot.get_bounds()

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
            i = (i+1) % robot.get_joint_number()
            angle = limits[i][0]
            sense = limits[i][0] < limits[i][1]
            new_angle = False

        angles[i] = angle

        posture = my_robot.get_pos_from_matrix(matrixes=robot.get_posture(angles=angles))

        print("{} : {}     ".format(i, angle), end='\r')
        _draw_one_robot(posture=posture, end_point_color=(0, 0, 1), posture_color=(0, 0, 0), joint_color=(0, 1, 0.3), highlight=i)

        pg.display.flip()
        _event_handler()
        pg.time.wait(10)

def display_robot(posture : list, end_point_color=(0, 0, 1), posture_color=(0, 0, 0), circle=False, axes=True, z_up=True, size=(600, 600), background_color=(1, 1, 1), joint_color=(0, 1, 0.5)):
    """Dessine un nuage de point 3d.
    `posture` - Liste de points 3D definissant la posture du robot. Une liste de liste affichera plusieurs robots
    `end_point_color` - la couleur du dernier point du robot en (r, g, b) [0-1]. Default `(0, 0, 1)`
    `posture_color` - la couleur des sections du robot en (r, g, b) [0-1]. Default `(0, 0, 0)`
    `circle` - booleen pour l'affichage d'un cercle autour de l'axe Z de rayon 1. Default `False`
    `axes` - booleen pour l'affichage des axes. Default `True`
    `z_up` - booleen pour forcer l'axe Z vers le haut. Default `True`
    `size` - taille de la fenetre en (x, y). Default `(600, 600)`
    `background_color` - couleur du fond en (r, g, b) [0-1]. Default `(1, 1, 1)`
    `joint_color` - couleur des moteurs en (r, g, b) [0-1]. Default `(0, 1, 0.5)`"""

    _init_display(size, background_color, z_up)

    while _StaticVars.is_running:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)

        if axes:
            _draw_axes()

        if circle:
            _draw_circle()

        if isinstance(posture[0], list):
            for r in posture:
                _draw_one_robot(posture=r, end_point_color=end_point_color, posture_color=posture_color, joint_color=joint_color)
        else:
            _draw_one_robot(posture=posture, end_point_color=end_point_color, posture_color=posture_color, joint_color=joint_color)

        pg.display.flip()
        _event_handler()
        pg.time.wait(10)

def _draw_one_robot(posture : list, end_point_color : tuple, posture_color : tuple, joint_color : tuple, highlight_color=(1, 0, 0), highlight=None):
    # Chaque section est representee par un segment
    gl.glBegin(gl.GL_LINE_STRIP)
    gl.glColor3f(posture_color[0], posture_color[1], posture_color[2])

    for section in posture:
        gl.glVertex3f(section[0], section[1], section[2])

    gl.glEnd()


    # Chaque moteur est represente par une sphere
    for i in range(len(posture)):
        # Si on veux mettre en valeur un joint
        if highlight is not None and i == highlight+1:
            gl.glColor3f(highlight_color[0], highlight_color[1], highlight_color[2])
        else:
            # Mettre en valeur le end_point
            if i == len(posture)-1:
                gl.glColor3f(end_point_color[0], end_point_color[1], end_point_color[2])
            # Simple joint
            else:
                gl.glColor3f(joint_color[0], joint_color[1], joint_color[2])
        gl.glPushMatrix()
        gl.glTranslatef(posture[i][0], posture[i][1], posture[i][2])
        glu.gluSphere(glu.gluNewQuadric(), 0.003, 16, 16)
        gl.glPopMatrix()


def draw_points_cloud(points : list, point_color=(0, 0, 1), circle=False, axes=True, z_up=True, size=(600, 600), background_color=(1, 1, 1)):
    """Dessine un nuage de point 3d.
    `points` - les coordonnees des points en (x, y, z).
    `point_color` - la couleur de ces points en (r, g, b) [0-1]. Default `(0, 0, 1)`
    `circle` - booleen pour l'affichage d'un cercle autour de l'axe Z de rayon 1. Default `False`
    `axes` - booleen pour l'affichage des axes. Default `True`
    `z_up` - booleen pour forcer l'axe Z vers le haut. Default `True`
    `size` - taille de la fenetre en (x, y). Default `(600, 600)`
    `background_color` - couleur du fond en (r, g, b) [0-1]. Default `(1, 1, 1)`"""

    _init_display(size, background_color, z_up)

    while _StaticVars.is_running:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)

        if axes:
            _draw_axes()

        if circle:
            _draw_circle()

        gl.glBegin(gl.GL_POINTS)
        gl.glColor3f(point_color[0], point_color[1], point_color[2])

        for point in points:
            gl.glVertex3f(point[0], point[1], point[2])

        gl.glEnd()

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
    gl.glLineStipple(1, 0xaaaa)
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

def _draw_circle():
    gl.glBegin(gl.GL_LINE_LOOP)
    gl.glColor(0, 0, 0)

    SEGMENTS = 64

    for i in range(SEGMENTS):
        angle = float(i) * 2.0 * np.pi / SEGMENTS
        gl.glVertex3f(np.cos(angle), np.sin(angle), 0.0)

    gl.glEnd()

class _StaticVars:
    transl_factor = 1/120
    is_running = True
    mouse_left_pressed = False
    mouse_right_pressed = False
    mouse_last_x = 0
    mouse_last_y = 0
    mouse_x_axe = np.array(
        (
            (1, 0, 0, 0),
            (0, 1, 0, 0),
            (0, 0, 1, 0),
            (1, 0, 0, 1)
        )
    )
    mouse_y_axe = np.array(
        (
            (1, 0, 0, 0),
            (0, 1, 0, 0),
            (0, 0, 1, 0),
            (0, 1, 0, 1)
        )
    )

def _init_display(size : tuple, background_color : tuple, z_up : bool):
    pg.init()
    pg.display.set_mode(size, pg.OPENGL)

    # Perspective de vue du modele: fov, ratio, near & far clipping plane
    glu.gluPerspective(45, (size[0]/size[1]), 0.1, 50.0)

    # Reculer le point de vue pour voir la scene
    gl.glTranslatef(0.0, 0.0, -3)

    # De base, Z est un axe de profondeur (il viens vers la camera) et Y est vertical.
    if z_up:
        gl.glRotatef(-90, 1, 0, 0) # Mettre Z vers le haut, mais du coup Y est "loin"
        gl.glRotatef(180, 0, 0, 1) # Mettre Y vers la camera

    # Avoir le X (rouge) qui part a droite
    gl.glScalef(-1, 1, 1)

    # Couleur de fond
    gl.glClearColor(background_color[0], background_color[1], background_color[2], 1.0)

def _event_handler():
    _mouse_handler()
    for event in pg.event.get():
        _mouse_event(event)
        _closing_event(event)

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
        curr_y_axes = _StaticVars.mouse_y_axe.dot(matrix)
        curr_x_axes = _StaticVars.mouse_x_axe.dot(matrix)

        # Mise a jour de la derniere position
        _StaticVars.mouse_last_x = curr_x
        _StaticVars.mouse_last_y = curr_y

        if _StaticVars.mouse_right_pressed:
            # Effectuer une translation sur le repère de la caméra.
            # Un déplacement vertical doit être inversé.
            gl.glTranslatef(curr_x_axes[3][0]*(depl_x*_StaticVars.transl_factor), curr_x_axes[3][1]*(depl_x*_StaticVars.transl_factor), curr_x_axes[3][2]*(depl_x*_StaticVars.transl_factor))
            gl.glTranslatef(curr_y_axes[3][0]*(-depl_y*_StaticVars.transl_factor), curr_y_axes[3][1]*(-depl_y*_StaticVars.transl_factor), curr_y_axes[3][2]*(-depl_y*_StaticVars.transl_factor))


        elif _StaticVars.mouse_left_pressed:
            # Effectuer une rotation autour de ces axes (et non autour de l'axe monde).
            # Deplacer la souris horizontalement (x) fait tourner le monde sur l'axe vertical (y) et vice-versa.
            gl.glRotatef(-depl_x, curr_y_axes[3][0], curr_y_axes[3][1], curr_y_axes[3][2])
            gl.glRotatef(-depl_y, curr_x_axes[3][0], curr_x_axes[3][1], curr_x_axes[3][2])
