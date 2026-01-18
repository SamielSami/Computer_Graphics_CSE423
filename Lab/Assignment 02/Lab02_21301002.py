# id: 21301002

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_Width, W_Height = 700, 700
bskt_speed = 30
bskt_height = 10
bskt_width = 110
cord_basket = W_Width // 2
basket_color = (1.0, 1.0, 1.0)  # Initially white

diamond = None
diamond_size = 10
diamond_speed = 3
speed_increase_val = 800
time_count = 0
score = 0
game_over = False
paused = False

class Diamond:
    def __init__(self, x):
        self.x = x
        self.y = W_Height
        self.color = (random.random(), random.random(), random.random())  # Random bright color

    def fallen(self):
        self.y -= diamond_speed
        if self.y <= 0:
            return False
        return True

def midpoint_line(x0, y0, x1, y1):
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    mx = 1 if x0 < x1 else -1
    my = 1 if y0 < y1 else -1
    rr = dx - dy

    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        a = rr * 2

        if a < dx:
            rr += dx
            y0 += my

        if a > -dy:
            rr -= dy
            x0 += mx
    
    return points


def restart_game():
    global game_over, score, diamond, cord_basket, basket_color, diamond_speed, time_count
    game_over = False
    score = 0
    diamond = None
    diamond_speed = 3 
    diamond = Diamond(random.randint(0, W_Width))  
    cord_basket = W_Width // 2
    basket_color = (1.0, 1.0, 1.0)  # Reset basket color  
    time_count = 0  
    


def draw_basket(x):
    bottom_w = int(bskt_width * 0.6)
    h_bottom_w = bottom_w // 2
    h_top_w = bskt_width // 2
    top = bskt_height

    basket_lines = [
        (x - h_bottom_w, 0, x + h_bottom_w, 0),  # Bottom
        (x - h_bottom_w, 0, x - h_top_w, top),   # Left side
        (x + h_bottom_w, 0, x + h_top_w, top),   # Right side
        (x - h_top_w, top, x + h_top_w, top)     # Top
    ]

    for x0, y0, x1, y1 in basket_lines:
        for (px, py) in midpoint_line(x0, y0, x1, y1):
            glVertex2f(px, py)

def draw_diamond(x, y):
    d = diamond_size // 2

    diamond_lines = [
        (x - d, y, x, y + d),  # Left to Top
        (x, y + d, x + d, y),  # Top to Right
        (x + d, y, x, y - d),  # Right to Bottom
        (x, y - d, x - d, y)   # Bottom to Left
    ]

    for x0, y0, x1, y1 in diamond_lines:
        for (px, py) in midpoint_line(x0, y0, x1, y1):
            glVertex2f(px, py)

def check_collision(diamond):
    if (bskt_height >= diamond.y >= 0 and
        cord_basket - bskt_width // 2 <= diamond.x <= cord_basket + bskt_width // 2):
        return True
    return False

##########################################################

def cross_button(x, y, size):
    half2 = size // 2
    
    # Coordinates for "X"
    points = [
        (x - half2, y - half2, x + half2, y + half2),  # bottom-left to top-right
        (x - half2, y + half2, x + half2, y - half2)   # top-left to bottom-right
    ]
    
    for x0, y0, x1, y1 in points:
        for (px, py) in midpoint_line(x0, y0, x1, y1):
            glVertex2f(px, py)


def play_pause_button(x, y, size, paused):
    half1 = size // 2
    if paused:
        # Draw "play" icon 
        points = [
            (x - half1, y - half1),  
            (x - half1, y + half1),  
            (x + half1, y)              
        ]
    else:
        # Draw "pause" icon (two vertical bars)
        bar_width = size // 8
        points = [
            (x - half1, y + half1, x - half1, y - half1),  # Left bar
            (x + bar_width, y + half1, x + bar_width, y - half1)   # Right bar
        ]

    if paused:
        for i in range(3):
            i2 = (i + 1) % 3 
            for (px, py) in midpoint_line(points[i][0], points[i][1], points[i2][0], points[i2][1]):
                glVertex2f(px, py)
    else:
        for x0, y0, x1, y1 in points:
            for (px, py) in midpoint_line(x0, y0, x1, y1):
                glVertex2f(px, py)

   

def arrow_button(x, y, size):
    tip_x1 = x - size  # Arrow width is the same as size
    half_h = size // 2

    lines = [      
        (x + half_h, y + half_h, tip_x1, y),  
        (tip_x1, y, x + half_h, y - half_h)  ]

    for x0, y0, x1, y1 in lines:
        for (px, py) in midpoint_line(x0, y0, x1, y1):
            glVertex2f(px, py)


########################################################################
def display():
    global basket_color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)

    glBegin(GL_POINTS)
    glColor3f(*basket_color)
    draw_basket(cord_basket)
    
    glColor3f(1.0, 0.0, 0.0)  # Red color for cross button
    cross_button(W_Width - 50, W_Height - 50, 40)

    glColor3f(0.0, 1.0, 1.0)  # Bright teal color
    arrow_button(50, W_Height - 50, 40)

    glColor3f(1.0, 0.64, 0.0)  # Amber color for play/pause button
    play_pause_button(W_Width // 2, W_Height - 50, 40, paused)

   
    if diamond and not paused:
        if diamond.fallen():
            glColor3f(diamond.color[0], diamond.color[1], diamond.color[2])
            draw_diamond(diamond.x, diamond.y)
        else:
            global game_over
            game_over = True
            basket_color = (1.0, 0.0, 0.0) #red

    if game_over:
        print(f"Game Over! Score: {score}")
    else:
        print(f"Score: {score}")

    glEnd()
    glutSwapBuffers()

def animate():
    global score, diamond, game_over, time_count, diamond_speed

    if game_over:
        return

    # Handle diamond collision
    if diamond and check_collision(diamond):
        score += 1
        diamond = None

    # Spawn new diamond if none exists
    diamond = diamond or Diamond(random.randint(0, W_Width))
    time_count += 1
    if time_count % speed_increase_val == 0:
        diamond_speed += 0.5

    glutPostRedisplay()

#############################################################################

def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Convert mouse coordinates to OpenGL coordinates
        y = W_Height - y  
        
        # Button boundaries
        button_x = 50
        button_y = W_Height - 50
        button_size = 40
        
        if (button_x - button_size // 2 <= x <= button_x + button_size // 2 and
            button_y - button_size // 2 <= y <= button_y + button_size // 2):
            restart_game()
            print("Starting Over")
        # Play/Pause Button
        elif W_Width // 2 - 20 <= x <= W_Width // 2 + 20 and W_Height - 70 <= y <= W_Height - 30:
            global paused
            paused = not paused
        
        # Cross Button
        elif W_Width - 70 <= x <= W_Width - 30 and W_Height - 70 <= y <= W_Height - 30:
            print(f"Goodbye! Your score: {score}")
            glutLeaveMainLoop()  # Terminate the application

    glutPostRedisplay()


def specialKeyListener(key, x, y):
    global cord_basket
    if key == GLUT_KEY_LEFT:
        cord_basket = max(cord_basket - bskt_speed, bskt_width // 2)
    if key == GLUT_KEY_RIGHT:
        cord_basket= min(cord_basket + bskt_speed, W_Width - bskt_width // 2)

    glutPostRedisplay()
    
############################################################################

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, W_Width, 0, W_Height)

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"Catch the Diamond!")
init()
glutIdleFunc(animate)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouse)
glutDisplayFunc(display)
glutMainLoop()
