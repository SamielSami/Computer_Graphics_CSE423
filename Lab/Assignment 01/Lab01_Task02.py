from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

background_color = [0.0, 0.0, 0.0] 
li = []
point_size = 6  
speed = 1  
freeze = False  
initial_x=1 #speed of the ball 
initial_y=1


# Class for moving point
class Point_moving:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.x1 = random.choice([-1, 1]) * initial_x 
        self.y1 = random.choice([-1, 1]) * initial_y
        self.color = [random.random() for _ in range(3)] #set random 3 rgb
        self.original_color = self.color[:]
        
        self.blink_initial = 0
        self.blinking = False

    def moving(self):
        if not freeze:
            self.x += speed* self.x1
            self.y += speed* self.y1

            # Bounce off walls
            if self.x >= 500 or self.x <= 0 :
                self.x1 *= -1
            if self.y >= 500 or self.y <= 0  :
                self.y1 *= -1
    
    def drawing(self):
        if self.blinking:
            current_time = time.time()
            if current_time - self.blink_initial >= 0.5:
                self.color = self.original_color
                self.blinking = False
            else:
                self.color = background_color


        glColor3f(*self.color)
        glBegin(GL_POINTS)
        glVertex2f(self.x, self.y)
        glEnd()
    
    def start_blinking(self):
        self.blinking = True
        self.blink_initial = time.time()

# orthographic projection
def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# mouse clicks
def mouse_handler(button, state, x, y):
    if not freeze and button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        # Add a new moving point 
        a = Point_moving(x, 500 - y)
        li.append(a)
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        for point in li:
            point.start_blinking()

# special keys (arrow keys)
def specialkeys_handler(key, x, y):
    global speed
    if not freeze:
        if key == GLUT_KEY_UP:
            speed *= 2  
            print(f"Speed x{speed:.2f} ")
        elif key == GLUT_KEY_DOWN:
            speed /= 2  
            print(f"Speed x{speed:.2f} ")

# Keyboard keys
def keyboard_handler(key, x, y):
    global freeze
    if key == b' ':
        freeze = not freeze  # Toggle frozen state
        if freeze:
            print("Points freeze")
        else:
            print("Points resume")

# Display 
def show_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glPointSize(point_size)  # Set the size of the points
    for point in li:
        point.moving()
        point.drawing()
    glutSwapBuffers()

# updating the screen
def update(v):
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"MAGIC BOX")
glutDisplayFunc(show_screen)
glutMouseFunc(mouse_handler)
glutSpecialFunc(specialkeys_handler)
glutKeyboardFunc(keyboard_handler)
glutTimerFunc(16, update, 0)
glutMainLoop()
