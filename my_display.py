"""Fichier display contenant les fonctions d'affichage pour un robot.
Pour empecher le prompt de pygame, faire "export PYGAME_HIDE_SUPPORT_PROMPT=hide" """


import OpenGL.GL as gl
import OpenGL.GLU as glu
#import OpenGL.GLUT as glut
import numpy as np
import pygame as pg
#import pygame.locals as pgl

def display_robot(robot, postures=None, end_point_color=(0, 0, 255), posture_color=(0, 0, 0), circle=False, axes=True, z_up=True, size=(600, 600), background_color=(255, 255, 255)):
    """Dessine un nuage de point 3d.
    `robot` - Le robot de type `my_robot.Robot`
    `postures` - Liste de liste d'angle à faire executer au robot pour afficher differentes postures. Default `None`
    `end_point_color` - la couleur du dernier point du robot en (r, g, b) [0-255]. Default `(0, 0, 255)`
    `posture_color` - la couleur des sections du robot en (r, g, b) [0-255]. Default `(0, 0, 0)`
    `circle` - booleen pour l'affichage d'un cercle autour de l'axe Z de rayon 1. Default `False`
    `axes` - booleen pour l'affichage des axes. Default `True`
    `z_up` - booleen pour forcer l'axe Z vers le haut. Default `True`
    `size` - taille de la fenetre en (x, y). Default `(600, 600)`
    `background_color` - couleur du fond en (r, g, b) [0-255]. Default `(255, 255, 255)`"""

    _init_display(size, background_color, z_up)

    while _StaticVars.is_running:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)

        if axes:
            _draw_axes()

        if circle:
            _draw_circle()

        if postures is not None:
            for angles in postures:
                robot.execute(angles)
                _draw_one_robot(robot=robot, end_point_color=end_point_color, draw_posture=True, posture_color=posture_color)
        else:
            _draw_one_robot(robot=robot, end_point_color=end_point_color, draw_posture=True, posture_color=posture_color)

        pg.display.flip()
        _event_handler()
        pg.time.wait(10)

def _draw_one_robot(robot, end_point_color, draw_posture, posture_color):

    if draw_posture:
        # Chaque section est representee par un segment
        gl.glBegin(gl.GL_LINE_STRIP)
        gl.glColor3f(posture_color[0], posture_color[1], posture_color[2])

        for section in robot.posture:
            gl.glVertex3f(section[0], section[1], section[2])

        gl.glEnd()

    # Dessiner la position du robot
    gl.glBegin(gl.GL_POINTS)
    gl.glColor3f(end_point_color[0], end_point_color[1], end_point_color[2])

    gl.glVertex3f(robot.end_point[0], robot.end_point[1], robot.end_point[2])

    gl.glEnd()

def draw_points_cloud(points, point_color=(0, 0, 255), circle=False, axes=True, z_up=True, size=(600, 600), background_color=(255, 255, 255)):
    """Dessine un nuage de point 3d.
    `points` - les coordonnees des points en (x, y, z).
    `point_color` - la couleur de ces points en (r, g, b) [0-255]. Default `(0, 0, 255)`
    `circle` - booleen pour l'affichage d'un cercle autour de l'axe Z de rayon 1. Default `False`
    `axes` - booleen pour l'affichage des axes. Default `True`
    `z_up` - booleen pour forcer l'axe Z vers le haut. Default `True`
    `size` - taille de la fenetre en (x, y). Default `(600, 600)`
    `background_color` - couleur du fond en (r, g, b) [0-255]. Default `(255, 255, 255)`"""

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
    gl.glColor3f(0, 0, 255)
    gl.glVertex3f(0, 0, 0)
    gl.glVertex3f(1, 0, 0)

    gl.glColor3f(0, 255, 0)
    gl.glVertex3f(0, 0, 0)
    gl.glVertex3f(0, 1, 0)

    gl.glColor3f(255, 0, 0)
    gl.glVertex3f(0, 0, 0)
    gl.glVertex3f(0, 0, 1)
    gl.glEnd()

def _draw_circle():
    gl.glBegin(gl.GL_LINE_LOOP)
    gl.glColor(0, 0, 0)

    for i in range(16):
        angle = float(i) * 2.0 * np.pi / 16
        gl.glVertex3f(np.cos(angle), np.sin(angle), 0.0)

    gl.glEnd()

class _StaticVars:
    is_running = True
    mouse_pressed = False
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

def _init_display(size, background_color, z_up):
    pg.init()
    pg.display.set_mode(size, pg.OPENGL)

    # Perspective de vue du modèle: fov, ratio, near & far clipping plane
    glu.gluPerspective(45, (size[0]/size[1]), 0.1, 50.0)

    # Reculer le point de vue pour voir la scène
    gl.glTranslatef(0.0, 0.0, -3)

    if z_up:
        gl.glRotatef(-90, 1, 0, 0)
        gl.glRotatef(180, 0, 0, 1)

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
            _StaticVars.mouse_pressed = True
            _StaticVars.mouse_last_x, _StaticVars.mouse_last_y = pg.mouse.get_pos()

        # Wheel Up
        elif event.button == 4:
            gl.glScalef(1.5, 1.5, 1.5)

        elif event.button == 5:
            gl.glScalef(0.6, 0.6, 0.6)

    elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
        _StaticVars.mouse_pressed = False

def _mouse_handler():
    if _StaticVars.mouse_pressed:
        # Position actuelle de la souris
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

        # Effectuer une rotation autour de ces axes (et non autour de l'axe monde).
        # Deplacer la souris horizontalement (x) fait tourner le monde sur l'axe vertical (y) et vice-versa.
        gl.glRotatef(depl_x, curr_y_axes[3][0], curr_y_axes[3][1], curr_y_axes[3][2])
        gl.glRotatef(depl_y, curr_x_axes[3][0], curr_x_axes[3][1], curr_x_axes[3][2])

        # Mise a jour de la derniere position
        _StaticVars.mouse_last_x = curr_x
        _StaticVars.mouse_last_y = curr_y
