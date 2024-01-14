import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1),
)

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6),
)

normals = [
    (0, 0, -1),
    (-1, 0, 0),
    (0, 0, 1),
    (1, 0, 0),
    (0, 1, 0),
    (0, -1, 0)
]

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7),
)


def cube():
    glBegin(GL_QUADS)
    for i_surface, surface in enumerate(surfaces):
        glColor3fv((0.0, 0.8, 0.0))
        glNormal3fv(normals[i_surface])
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def light():
    glLight(GL_LIGHT0, GL_POSITION, (-5, 0, 0, 0))


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    clock = pygame.time.Clock()

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0, 0, -13)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)

    light()

    angle = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    glTranslatef(0, 0.5, 0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0, -0.5, 0)
                if event.key == pygame.K_o:
                    glTranslatef(sin(radians(angle)), 0, -cos(radians(angle)))
                if event.key == pygame.K_i:
                    glTranslatef(-sin(radians(angle)), 0, cos(radians(angle)))
                if event.key == pygame.K_LEFT:
                    glTranslatef(cos(radians(angle)), 0, sin(radians(angle)))
                if event.key == pygame.K_RIGHT:
                    glTranslatef(-cos(radians(angle)), 0, -sin(radians(angle)))

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotatef(0.5, 0, 1, 0)
        angle += 0.5
        angle = angle % 360
        cube()
        pygame.display.flip()
        clock.tick(60)


main()
