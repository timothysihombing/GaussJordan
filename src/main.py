# File main.py
# Abram Perdanaputra      / 13516083
# Timothy AH Sihombing    / 13516090
#
# TUGAS BESAR 2 ALJABAR GEOMETRI

import threading
import numpy as np
import time

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from GLObject import *

#from inputController import userInput

window = 0                                             # glut window number
width, height = 800, 600                               # window size

current_polygon = Object2d()

colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (0,1,1),
    )

def clear():
    print("\n" * 100)

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the screen
    glLoadIdentity()                                   # reset position
    refresh2d(width, height)

    # draw coordinate lines
    glColor3f(1, 2, 1.0)
    drawCoord(width, height)

    # draw polygon
    glColor3f(1, 1, 1)
    drawPolygon(current_polygon)

    glutSwapBuffers()                                  # important for double buffering


def drawCoord(width, height):
    glBegin(GL_LINES)
    glVertex2f(-width,0)
    glVertex2f(width,0)
    glEnd()

    glBegin(GL_LINES)
    glVertex2f(0,-height)
    glVertex2f(0,height)
    glEnd()

def drawPolygon(polygon):
    glBegin(GL_POLYGON)
    x = 0
    for vertex in polygon.vertices():
        x+=1
        glColor3fv(colors[x])
        glVertex2f(vertex[0], vertex[1])

    glEnd()

def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1 * width / 2, width / 2, -1 * height / 2, height / 2, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def animate(polygon, next_polygon, duration, interval):
    elapsed_time = 0;

    delta = (next_polygon.matrix - polygon.matrix) / (duration / interval)

    while elapsed_time < duration:
        polygon.matrix += delta
        elapsed_time += interval
        time.sleep(interval)

def userInput():
    clear()
    base_polygon = Object2d()
    global current_polygon

    print("""
  /$$$$$$                                 /$$$$$$  /$$
 /$$__  $$                               /$$__  $$| $$
| $$  \ $$  /$$$$$$   /$$$$$$  /$$$$$$$ | $$  \__/| $$
| $$  | $$ /$$__  $$ /$$__  $$| $$__  $$| $$ /$$$$| $$
| $$  | $$| $$  \ $$| $$$$$$$$| $$  \ $$| $$|_  $$| $$
| $$  | $$| $$  | $$| $$_____/| $$  | $$| $$  \ $$| $$
|  $$$$$$/| $$$$$$$/|  $$$$$$$| $$  | $$|  $$$$$$/| $$$$$$$$
 \______/ | $$____/  \_______/|__/  |__/ \______/ |________/
          | $$
          | $$
          |__/


""")
    while True:

        print("Instruksi yang dapat dieksekusi :")
        print("<===================================================================================>")
        print("||   draw2d                      |   Input titik-titik yang akan digambar          ||")
        # print("draw3d <n>                  ||   ")
        print("||   translate <dx> <dy>         |   Input besar pergeseran                        ||")
        print("||   dilate    <k>               |   Input faktor dilatasi                         ||")
        print("||   rotate    <deg> <a> <b>     |   Input besar perputaran dan titik poros        ||")
        print("||   reflect   <param>           |   Input sumbu pencerminan                       ||")
        print("||   shear     <param> <k>       |   Input sumbu dan faktor shear                  ||")
        print("||   stretch   <param> <k>       |   Input sumbu dan faktor peregangan             ||")
        print("||   custom    <a> <b> <c> <d>   |   Input matriks transformasi                    ||")
        print("||   multiple  <n>               |   Input jumlah instruksi yang akan dilakukan    ||")
        print("||   reset                       |                                                 ||")
        print("||   exit                        |                                                 ||")
        print("<===================================================================================>")
        print("                                       BY:                                           ")
        print("                            Abram Perdanaputra / 13516083                            ")
        print("                          Timothy AH Sihombing / 13516090                            ")
        print("")

        print("Masukan instruksi :")
        string = input(">> ")
        query = []
        query = string.split(' ')

        if query[0] == 'draw2d':
            # fungsi draw2d
            if len(query) != 1:
                print("Wrong input.")
            else:
                # cast the arguments to float
                points = int(input("Masukan jumlah titik : "))
                for i in range(points):
                    inp = input("Masukan titik {} : ".format(i + 1))
                    inp = inp.split(" ")
                    query.extend(inp)


                i = 1;
                j = 2;
                k = 0;

                mat = np.zeros((2, int(len(query) / 2)))
                while i < len(query) and j < len(query) + 1:
                    mat[0, k] = query[i]
                    mat[1, k] = query[j]
                    i += 2
                    j += 2
                    k += 1
                current_polygon = Object2d(mat)
                base_polygon = current_polygon.copyObject()


        elif query[0] == 'translate':
            #fungsi translate
            if len(query) != 3:
                print("Wrong input.")
            else:
                query[1] = float(query[1])
                query[2] = float(query[2])
                next_polygon = current_polygon.translate(query[1], query[2])
                animate(current_polygon, next_polygon, 0.5, 0.001)

        elif query[0] == 'dilate':
            #fungsi dilate
            if len(query) != 2:
                print("Wrong input.")
            else:
                query[1] = float(query[1])
                next_polygon = current_polygon.dilate(query[1])
                animate(current_polygon, next_polygon, 0.5, 0.001)

        elif query[0] == 'rotate':
            #fungsi rotate
            if len(query) != 4:
                print("Wrong input.")
            else:
                query[1] = float(query[1])
                query[2] = float(query[2])
                query[3] = float(query[3])
                next_polygon = current_polygon.rotate(query[1], query[2], query[3])
                animate(current_polygon, next_polygon, 0.5, 0.001)

        elif query[0] == 'reflect':
            #fungsi reflect
            if len(query) != 2:
                print("Wrong input.")
            else:
                next_polygon = current_polygon.reflect(query[1])
                animate(current_polygon, next_polygon, 0.5, 0.001)

        elif query[0] == 'shear':
            #fungsi shear
            if len(query) != 3:
                print("Wrong input.")
            else:
                query[2] = float(query[2])
                next_polygon = current_polygon.shear(query[1], query[2])
                animate(current_polygon, next_polygon, 0.5, 0.001)

        elif query[0] == 'stretch':
            #fungsi stretch
            if len(query) != 3:
                print("Wrong input.")
            else:
                query[2] = float(query[2])
                next_polygon = current_polygon.stretch(query[1], query[2])
                animate(current_polygon, next_polygon, 0.5, 0.001)

        elif query[0] == 'custom':
            #fungsi custom
            if len(query) != 5:
                print("Wrong input.")
            else:
                for i in range(1, len(query)):
                    query[i] = float(query[i])
                next_polygon = current_polygon.custom(query[1], query[2], query[3], query[4])
                animate(current_polygon, next_polygon, 0.5, 0.001)

        elif query[0] == 'multiple':
            #fungsi multiple
            if len(query) != 2:
                print("Wrong input.")
            else:
                command = []
                for i in range(int(query[1])):
                    inp = input()
                    inp = inp.split(" ")
                    command.extend(inp)
                executeCommand(command)

        elif query[0] == 'reset':
            #fungsi reset
            if len(query) != 1:
                print("Wrong input.")
            else:
                next_polygon = base_polygon.copyObject()
                animate(current_polygon, next_polygon, 0.5, 0.001)

        elif query[0] == 'exit':
            #fungsi exit
            if len(query) != 1:
                print("Wrong input.")
            else:
                os._exit(1)

        else:
            print("Retry, wrong input")
        print("")

def executeCommand(query):
    global current_polygon
    base_polygon = Object2d()

    temp_polygon = current_polygon.copyObject()

    while len(query) > 0:
        if query[0] == 'translate':
            del query[0]
            #fungsi translate
            dx = float(query[0])
            del query[0]
            dy = float(query[0])
            del query[0]
            temp_polygon = temp_polygon.translate(dx, dy)

        elif query[0] == 'dilate':
            del query[0]
            #fungsi dilate
            temp = float(query[0])
            del query[0]
            temp_polygon = temp_polygon.dilate(temp)

        elif query[0] == 'rotate':
            del query[0]
            #fungsi rotate
            deg = float(query[0])
            del query[0]
            a = float(query[0])
            del query[0]
            b = float(query[0])
            del query[0]
            temp_polygon = temp_polygon.rotate(deg, a, b)

        elif query[0] == 'reflect':
            del query[0]
            #fungsi reflect
            temp_polygon = temp_polygon.reflect(query[0])
            del query[0]

        elif query[0] == 'shear':
            del query[0]
            #fungsi shear
            param = query[0]
            del query[0]
            a = float(query[0])
            del query[0]
            temp_polygon = temp_polygon.shear(param, a)

        elif query[0] == 'stretch':
            del query[0]
            #fungsi stretch
            param = query[0]
            del query[0]
            a = float(query[0])
            del query[0]
            temp_polygon = temp_polygon.stretch(param, a)

        elif query[0] == 'custom':
            del query[0]
            #fungsi custom
            a = float(query[0])
            del query[0]
            b = float(query[0])
            del query[0]
            c = float(query[0])
            del query[0]
            d = float(query[0])
            del query[0]

            temp_polygon = temp_polygon.custom(a, b, c, d)

        elif query[0] == 'reset':
            #fungsi reset
            temp_polygon = base_polygon.copyObject()
            del query[0]

        else:
            print("Wrong input.")
    next_polygon = temp_polygon.copyObject()
    animate(current_polygon, next_polygon, 0.5, 0.001)


def GLUT():
    # GLUT initialization
    glutInit()                                             # initialize glut
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(width, height)                      # set window size
    glutInitWindowPosition(0, 0)                           # set window position
    window = glutCreateWindow("Santuy Original")           # create window with title
    glutDisplayFunc(draw)                                  # set draw function callback
    glutIdleFunc(draw)                                     # draw all the time
    glutMainLoop()

# 2nd Thread
thread2 = threading.Thread(target = userInput)
thread2.daemon = True
thread2.start()

GLUT()
