from Robots import Arm2D
import numpy as np

#Pour empêcher pygame de print au début du programme
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import random

#Nombre de morceau pour faire le cercle extérieur
SIDE_NUM_EXT_CIRCLE = 80

#Nombre de morceau pour faire un cercle à chaque jonction du bras
SIDE_NUM_JOINT = 16

#Taille d'un cercle à chaque jonction du bras
JOINT_SIZE = 0.02


def init_display(size_x, size_y, background_color=(255, 255, 255)):
    pygame.init()
    pygame.display.set_mode((size_x,size_y), OPENGL)

    # Perspective de vue du modèle: fov, ratio, near & far clipping plane
    gluPerspective(45, (size_x/size_y), 0.1, 50.0)

    # Reculer le point de vue pour voir la scène
    glTranslatef(0.0, 0.0, -3)

    # Tourner l'image pour que l'angle 0 pointe vers le haut
    glRotate(90.0, 0.0, 0.0, 1.0)

    glClearColor(background_color[0], background_color[1], background_color[2], 1.0)

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    pygame.display.flip()
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)    

def closing_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or ( event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) :
            pygame.quit()
            print()
            sys.exit(0)

def drawCircle(color=(0, 0, 0)):
    glColor(color[0], color[1], color[2])
    glBegin(GL_LINE_LOOP)
    for i in range(SIDE_NUM_EXT_CIRCLE):
        angle = float(i) * 2.0 * np.pi / SIDE_NUM_EXT_CIRCLE
        glVertex3f(np.cos(angle), np.sin(angle), 0.0)
    glEnd()

def draw2Drobot(robot, circle, arm):
    glColor3f(0, 0, 0)
    #Dessiner le cercle entourant le robot
    if circle:
        drawCircle()
    #Déssiner chaques jonctions, ainsi que des cercles à chaque jonctions
    if arm:
        #Affichage des ségments pour chaques jonctions
        glBegin(GL_LINE_STRIP)
        for section in robot.posture:
            glVertex3f(section[0], section[1], 0.0)
        glEnd()

        #Affichage des cercles entre chaques jonctions
        nb = 0
        for section in robot.posture:
            nb+=1
            glBegin(GL_POLYGON)
            for i in range(SIDE_NUM_JOINT):
                angle = float(i) * 2.0 * np.pi / SIDE_NUM_JOINT
                if nb == robot.dim+1:
                    glColor3f(0, 50, 230)
                glVertex3f(np.cos(angle) * JOINT_SIZE + section[0], np.sin(angle) * JOINT_SIZE + section[1], 0.0)
            glEnd()
    
    glColor3f(0, 0, 150)
    glBegin(GL_POINTS)
    glVertex3f(robot.end_point[0], robot.end_point[1], 0.0)
    glEnd()

def motor_babling(robot, step=5000, circle=True, arm=False, size_x=600, size_y=600):
    """Affiche un robot avec un motor babling pendant `step` étapes.
    De base n'affiche que la position finale de ce robot"""
    init_display(size_x=size_x, size_y=size_y)

    if circle:
        drawCircle()

    batch = step/10

    for i in range(step):
        if i%batch == 0:
            print('[', end='')
            for j in range(10):
                if j/10 < i/step:
                    print('#', end='')
                else:
                    print('_', end='')
            print(']', end='\r')
            closing_event()

        robot.execute([random.uniform(-robot.limit, robot.limit) for _ in range(robot.dim)])

        draw2Drobot(robot, circle=False, arm=arm)
        
    
    pygame.display.flip()

    print("done        ")

    while True:
        closing_event()
        pygame.time.wait(10)

def draw_one_2d_robot(robot, circle=True, arm=True, size_x=600, size_y=600):
    init_display(size_x, size_y)

    draw2Drobot(robot=robot, circle=circle, arm=arm)

    pygame.display.flip()

    while True:
        closing_event()
        pygame.time.wait(10)
