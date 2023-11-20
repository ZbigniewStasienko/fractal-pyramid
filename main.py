import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

def draw_triangle(v1, v2, v3):
    glBegin(GL_TRIANGLES)
    glVertex3fv(v1)
    glVertex3fv(v2)
    glVertex3fv(v3)
    glEnd()

def midpoint(p1, p2):
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, (p1[2] + p2[2]) / 2)

def sierpinski(v1, v2, v3, v4, level):
    if level == 0:
        draw_triangle(v1, v2, v3)
        draw_triangle(v1, v2, v4)
        draw_triangle(v1, v3, v4)
        draw_triangle(v2, v3, v4)
        return

    mid1 = midpoint(v1, v2)
    mid2 = midpoint(v2, v3)
    mid3 = midpoint(v3, v1)
    mid4 = midpoint(v1, v4)
    mid5 = midpoint(v2, v4)
    mid6 = midpoint(v3, v4)

    sierpinski(v1, mid1, mid3, mid4, level - 1)
    sierpinski(mid1, v2, mid2, mid5, level - 1)
    sierpinski(mid3, mid2, v3, mid6, level - 1)
    sierpinski(mid4, mid5, mid6, v4, level - 1)

def main():
    level = int(input("Podaj poziom piramidy (zalecane max 5): "))

    if level < 0:
        return

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, -1.0, -5)
    surface_condition = 0
    angle = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    if surface_condition == 0:
                        surface_condition = 1
                    else:
                        surface_condition = 0

                if event.key == pygame.K_UP:
                    glTranslatef(0, -0.5, 0)

                if event.key == pygame.K_DOWN:
                    glTranslatef(0, 0.5, 0)

                if event.key == pygame.K_o:
                    glTranslatef(sin(radians(angle)), 0, -cos(radians(angle)))

                if event.key == pygame.K_i:
                    glTranslatef(-sin(radians(angle)), 0, cos(radians(angle)))

                if event.key == pygame.K_LEFT:
                    glTranslatef(cos(radians(angle)), 0, sin(radians(angle)))

                if event.key == pygame.K_RIGHT:
                    glTranslatef(-cos(radians(angle)), 0, -sin(radians(angle)))

        glRotatef(0.5, 0, 1, 0)
        angle += 0.5
        angle = angle % 360

        if surface_condition == 1:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        sierpinski((-1, 0, sqrt(3)/3), (1, 0, sqrt(3)/3), (0, 0, -sqrt(3)*2/3), (0, sqrt(15)/3, 0), level)
        pygame.display.flip()
        pygame.time.wait(10)

main()
