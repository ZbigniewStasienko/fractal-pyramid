from tkinter import messagebox

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *
from PIL import Image
import tkinter as tk


name_of_file = 'camo.JPG'
name_of_floor = 'floor.JPG'
instruction = "Strzalki: ruch kamery \nI: zoom in \nO:   zoom out \nScroll myszki: zoom in/zoom out \nS: wylaczenie/wlaczenie tekstury \nM: zwiekszenie poziomu rekurencji \nL: zmniejszenie poziomu rekurencji"

#Funkcja rysujaca trojkat w 3d na podstawie podanych wierzchołków
#oraz rozpinająca teksturę na ścianach
def draw_triangle(v1, v2, v3, txt_id):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, txt_id)
    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.0, 0.0)
    glVertex3fv(v1)
    glTexCoord2f(1.0, 0.0)
    glVertex3fv(v2)
    glTexCoord2f(0.0, 1.0)
    glVertex3fv(v3)
    glEnd()
    glDisable(GL_TEXTURE_2D)


#Funkcja wyznaczająca wspołrzędne (x,y,z) śrdoka pomiędzy dwoma punktami
#Niezbędna do generowania piramidy
def midpoint(p1, p2):
    return (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, (p1[2] + p2[2]) / 2


#Funckja rekurencyjne rysująca piramidę w 3d na podstawie aktualnego poziomu piramidy
def sierpinski(v1, v2, v3, v4, level, texture):
    if level == 0:
        draw_triangle(v1, v2, v3, texture)
        draw_triangle(v1, v2, v4, texture)
        draw_triangle(v1, v3, v4, texture)
        draw_triangle(v2, v3, v4, texture)
        return

    mid1 = midpoint(v1, v2)
    mid2 = midpoint(v2, v3)
    mid3 = midpoint(v3, v1)
    mid4 = midpoint(v1, v4)
    mid5 = midpoint(v2, v4)
    mid6 = midpoint(v3, v4)

    sierpinski(v1, mid1, mid3, mid4, level - 1, texture)
    sierpinski(mid1, v2, mid2, mid5, level - 1, texture)
    sierpinski(mid3, mid2, v3, mid6, level - 1, texture)
    sierpinski(mid4, mid5, mid6, v4, level - 1, texture)


#Funkcja dodająca podłoże do projektu wczytując odpowiednią teksturę
def floor(angle, texture):
    glPushAttrib(GL_CURRENT_BIT)
    glPushMatrix()
    glRotatef(angle, 0.0, 1.0, 0.0)

    square_vertices = [
        (40.0, 0.0, 40.0),
        (-40.0, 0.0, 40.0),
        (-40.0, 0.0, -40.0),
        (40.0, 0.0, -40.0)
    ]
    texture_values = [
        (1.0, 1.0),
        (-1.0, 1.0),
        (-1.0, -1.0),
        (1.0, -1.0)
    ]
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    i = 0
    for vertex in square_vertices:
        glTexCoord2f(texture_values[i][0], texture_values[i][1])
        glVertex3fv(vertex)
        i += 1
    glEnd()
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()
    glPopAttrib()


#Funckja wczytująca teksturę z pliku do programu
def load_texture(file):
    try:
        image = Image.open(file)
    except Exception as exeption:
        print(f"Blad podczas otwierania pliku z tekstura: {exeption}")
        return None

    image_data = image.tobytes("raw", "RGB", 0, -1)
    width, height = image.size
    text_id = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, text_id)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    return text_id


#Funckja wyświetlająca instrukcję obsługi
def display_popup(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Instrukacja obslugi", message)
    root.destroy()


def main():
    print("!!!ABY WYSWIETLIC INSTRUKCJE OBSLUGI WCISNIJ P PODCZAS DZIALANIA PROGRAMU!!!")
    level = int(input("Podaj poziom piramidy (liczba od 0 do 6): "))

    if level < 0 or level > 6:
        print("Niepoprawny rozmiar")
        return

    #inicjalizacja okna pygame wraz z podstawowymi parametrami
    pygame.init()
    display = (1200, 700)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0.0, -1.0, -5)

    texture_id = load_texture(name_of_file)
    texture_id2 = load_texture(name_of_floor)

    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)

    surface_condition = 0
    angle = 0
    #Główna pętla w programie nasłuchująca zdarzeń z klawiatury
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                glTranslatef(sin(radians(angle)), 0, -cos(radians(angle)))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                glTranslatef(-sin(radians(angle)), 0, cos(radians(angle)))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    if surface_condition == 0:
                        surface_condition = 1
                    else:
                        surface_condition = 0

                if event.key == pygame.K_UP:
                    glTranslatef(0, -1, 0)

                if event.key == pygame.K_DOWN:
                    glTranslatef(0, 1, 0)

                if event.key == pygame.K_o:
                    glTranslatef(sin(radians(angle)), 0, -cos(radians(angle)))

                if event.key == pygame.K_i:
                    glTranslatef(-sin(radians(angle)), 0, cos(radians(angle)))

                if event.key == pygame.K_LEFT:
                    glTranslatef(cos(radians(angle)), 0, sin(radians(angle)))

                if event.key == pygame.K_RIGHT:
                    glTranslatef(-cos(radians(angle)), 0, -sin(radians(angle)))

                if event.key == pygame.K_m:
                    if level < 5:
                        level += 1

                if event.key == pygame.K_l:
                    if level > 0:
                        level -= 1

                if event.key == pygame.K_p:
                    display_popup(instruction)

        #obrót bryły
        glRotatef(0.5, 0, 1, 0)
        angle += 0.5
        angle = angle % 360

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #wyłączenie/włączenie tekstury
        if surface_condition == 1:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            sierpinski((-1, 0, sqrt(3) / 3), (1, 0, sqrt(3) / 3), (0, 0, -sqrt(3) * 2 / 3), (0, sqrt(15) / 3, 0), level, texture_id)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            sierpinski((-1, 0, sqrt(3) / 3), (1, 0, sqrt(3) / 3), (0, 0, -sqrt(3) * 2 / 3), (0, sqrt(15) / 3, 0), level, texture_id)

        floor(-angle, texture_id2)
        pygame.display.flip()
        pygame.time.wait(10)


main()
