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


def init_display(size_x, size_y, background_color=(255, 255, 255), is_2d=False):
    pygame.init()
    pygame.display.set_mode((size_x, size_y), OPENGL)

    # Perspective de vue du modèle: fov, ratio, near & far clipping plane
    gluPerspective(45, (size_x/size_y), 0.1, 50.0)

    # Reculer le point de vue pour voir la scène
    glTranslatef(0.0, 0.0, -3)

    # Tourner l'image pour que l'angle 0 pointe vers le haut
    if is_2d:
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

def drawCircle(circle_color=(0, 0, 0)):
    glColor(circle_color[0], circle_color[1], circle_color[2])
    glBegin(GL_LINE_LOOP)
    for i in range(SIDE_NUM_EXT_CIRCLE):
        angle = float(i) * 2.0 * np.pi / SIDE_NUM_EXT_CIRCLE
        glVertex3f(np.cos(angle), np.sin(angle), 0.0)
    glEnd()

def draw2Drobot(robot, draw_arm=False, arm_color=(0, 0, 0), end_joint_color=(0, 0, 150)):
    glColor3f(arm_color[0], arm_color[1], arm_color[2])
    #Déssiner chaques jonctions, ainsi que des cercles à chaque jonctions
    if draw_arm:
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
                    glColor3f(end_joint_color[0], end_joint_color[1], end_joint_color[2])
                glVertex3f(np.cos(angle) * JOINT_SIZE + section[0], np.sin(angle) * JOINT_SIZE + section[1], 0.0)
            glEnd()
    
    glColor3f(end_joint_color[0], end_joint_color[1], end_joint_color[2])
    glBegin(GL_POINTS)
    glVertex3f(robot.end_point[0], robot.end_point[1], 0.0)
    glEnd()

def draw_one_2d_robot(robot, draw_circle=True, draw_arm=True, size_x=600, size_y=600, arm_color=(0, 0, 0), end_joint_color=(0, 0, 150), background_color=(255, 255, 255), circle_color=(0, 0, 0)):
    init_display(size_x, size_y, background_color=background_color, is_2d=True)

    if draw_circle:
        drawCircle(circle_color=circle_color)

    draw2Drobot(robot=robot, draw_arm=draw_arm, arm_color=arm_color, end_joint_color=end_joint_color)

    pygame.display.flip()

    while True:
        closing_event()
        pygame.time.wait(10)

def draw3Drobot(robot, draw_arm=False, arm_color=(0, 0, 0), end_joint_color=(0, 0, 150)):
    glColor3f(arm_color[0], arm_color[1], arm_color[2])

    #Déssiner chaques jonctions, ainsi que des cercles à chaque jonctions
    if draw_arm:
        #Affichage des ségments pour chaques jonctions
        glBegin(GL_LINE_STRIP)
        for section in robot.posture:
            glVertex3f(section[0], section[1], section[2])
        glEnd()
    
    glColor3f(end_joint_color[0], end_joint_color[1], end_joint_color[2])
    glBegin(GL_POINTS)
    glVertex3f(robot.end_point[0], robot.end_point[1], robot.end_point[2])
    glEnd()

def draw_one_3d_robot(robot, draw_arm=True, size_x=600, size_y=600, arm_color=(0, 0, 0), end_joint_color=(0, 0, 150), background_color=(255, 255, 255)):
    init_display(size_x=size_x, size_y=size_y, background_color=background_color)

    my_mouse = MouseController()

    while True:
        my_mouse.control()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        draw_axes()

        draw3Drobot(robot=robot, draw_arm=draw_arm, arm_color=arm_color, end_joint_color=end_joint_color)

        pygame.display.flip()

        closing_event()
        pygame.time.wait(10)

def draw_multiple_3d_robot(robot, angles, draw_arm=True, size_x=600, size_y=600, arm_color=(0, 0, 0), end_joint_color=(0, 0, 150), background_color=(255, 255, 255)):
    init_display(size_x=size_x, size_y=size_y, background_color=background_color)

    my_mouse = MouseController()

    while True:
        my_mouse.control()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        draw_axes()

        for a in angles:
            robot.execute(a)
            draw3Drobot(robot=robot, draw_arm=draw_arm, arm_color=arm_color, end_joint_color=end_joint_color)

        pygame.display.flip()

        closing_event()
        pygame.time.wait(10)


class MouseController():

    def __init__(self):
        self.isPressed = False
        self.last_x = 300
        self.last_y = 300
        self.y_axe = np.array(
            (
                (1, 0, 0, 0),
                (0, 1, 0, 0),
                (0, 0, 1, 0),
                (0, 1, 0, 1)
            )
        )
        self.x_axe = np.array(
            (
                (1, 0, 0, 0),
                (0, 1, 0, 0),
                (0, 0, 1, 0),
                (1, 0, 0, 1)
            )
        )

    def control(self):
        # Check unpressed
        if not pygame.mouse.get_pressed()[0]:
            self.isPressed = False

        # Check position et rotate
        if self.isPressed:
            x,y = pygame.mouse.get_pos()
            curr_x, curr_y = x-self.last_x, y-self.last_y

            matrix = np.linalg.inv(glGetFloatv(GL_MODELVIEW_MATRIX))
            matrix[3] = (0, 0, 0, 1)
            curr_y_axes = self.y_axe.dot(matrix)
            curr_x_axes = self.x_axe.dot(matrix)

            glRotatef(curr_x, curr_y_axes[3][0], curr_y_axes[3][1], curr_y_axes[3][2])
            glRotatef(curr_y, curr_x_axes[3][0], curr_x_axes[3][1], curr_x_axes[3][2])

            self.last_x = x
            self.last_y = y

        # Check pressed
        if pygame.mouse.get_pressed()[0]:
            self.isPressed = True
            self.last_x, self.last_y = pygame.mouse.get_pos()

def draw_cloud(points, size_x=600, size_y=600, point_color=(0, 0, 150), background_color=(255, 255, 255)):
    init_display(size_x=size_x, size_y=size_y, background_color=background_color)

    my_mouse = MouseController()

    while True:
        my_mouse.control()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        draw_axes()

        glBegin(GL_POINTS)
        glColor3f(point_color[0], point_color[1], point_color[2])

        for p in points:
            glVertex3f(p[0], p[1], p[2])

        glEnd()

        pygame.display.flip()

        closing_event()
        pygame.time.wait(10)

def draw_axes():
    glBegin(GL_LINES)
    glColor3f(0, 0, 255)
    glVertex3f(0, 0, 0)
    glVertex3f(1, 0, 0)

    glColor3f(0, 255, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 1, 0)

    glColor3f(255, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 1)
    glEnd()
