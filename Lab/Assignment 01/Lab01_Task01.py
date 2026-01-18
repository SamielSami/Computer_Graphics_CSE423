from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

#rain_enabled = False
background_color = [1.0, 1.0, 1.0]  # Initial background white
rain_color = [0.0, 0.0, 0.0]  # Initial rain is black
rain_bend = 0

# Function to draw house
def draw_house():
    glLineWidth(3)
    glBegin(GL_LINES)
    
    # House structure
    glColor3f(0.0, 0.5, 1.0)  # blue 
    glVertex2f(100, 300)
    glVertex2f(400, 300)
    glVertex2f(100, 100)
    glVertex2f(400, 100)
    glVertex2f(100, 100)
    glVertex2f(100, 300)
    glVertex2f(400, 100)
    glVertex2f(400, 300)
    
    # Roof
    glVertex2f(100, 300)
    glVertex2f(250, 400)
    glVertex2f(400, 300)
    glVertex2f(250, 400)

    # Door
    glVertex2f(140, 200)
    glVertex2f(190, 200)
    glVertex2f(190, 200)
    glVertex2f(190, 100)
    glVertex2f(140, 200)
    glVertex2f(140, 100)

    # Window
    glVertex2f(280, 180)
    glVertex2f(350, 180)
    glVertex2f(280, 240)
    glVertex2f(350, 240)
    glVertex2f(280, 180)
    glVertex2f(280, 240)
    glVertex2f(350, 180)
    glVertex2f(350, 240)

    glVertex2f(315, 180)
    glVertex2f(315, 240)
    glVertex2f(280, 210)
    glVertex2f(350, 210)

    glEnd()

# background color
def color_background():
    glClearColor(*background_color, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)


# Draw raindrops 
def draw_rain():
    glLineWidth(2)
    glBegin(GL_LINES)
    for _ in range(50):  # Draw 50 raindrops
        x = random.randint(0, 500)
        y = random.randint(0, 500)
        glColor3f(*rain_color)  # Raindrop color
        glVertex2f(x, y)
        glVertex2f(x + rain_bend, y - 10)  # Raindrop length with=y, bending +x
    glEnd()



# orthographic projection
def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


# arrow keys to BEND rain
def rain_bending(key, x, y):
    global rain_bend
    if key == GLUT_KEY_RIGHT:
        rain_bend += 1
        print("Rain towards right")
    elif key == GLUT_KEY_LEFT:
        rain_bend -= 1
        print("Rain towards left")

# Day Night Cycle
def day_night(key, x, y):
    global background_color, rain_color
    if key == b'd':
        background_color = [1.0, 1.0, 1.0]  # White background
        rain_color = [0.0, 0.0, 0.0]  # Black raindrop 
        print("Day Time")
    elif key == b'n':
        background_color = [0.0, 0.0, 0.0]  # Black background
        rain_color = [1.0, 1.0, 1.0]  # White raindrop 
        print("Night Time")

# Display the scene
def show_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    color_background()
    draw_house()

    #if rain_enabled:
    draw_rain()
    glutSwapBuffers()

# updating the screen
def update_rain_time(a):
    glutPostRedisplay()
    glutTimerFunc(100, update_rain_time, 0)


# Initialize GLUT
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"House & Rain")
glutSpecialFunc(rain_bending)
glutKeyboardFunc(day_night)
glutDisplayFunc(show_screen)
glutTimerFunc(100, update_rain_time, 0)
glutMainLoop()
