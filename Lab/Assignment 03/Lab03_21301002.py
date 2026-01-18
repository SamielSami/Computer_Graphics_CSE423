# id: 21301002

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_Width, W_Height = 700, 700

darts = []
dart_radius = 5
dart_speed = 20

shooter_x = W_Width // 2
shooter_radius = 15
shooter_speed = 50

missed_circles = 0
score = 0
game_over = False
game_paused = False

btn_l_pos = (50, W_Height - 50)
btn_mid_pos = (W_Width // 2, W_Height - 50)
btn_r_pos = (W_Width - 50, W_Height - 50)
btn_size = 30

falling_circles = []
falling_speed = 2

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

# Check button click
def check_click(x, y, btn_center): 
    btn_x, btn_y = btn_center
    distnce = ((x - btn_x) ** 2 + (y - btn_y) ** 2) ** 0.6
    return distnce < btn_size

# Draw the Left Arrow Button
def left_arrow():
    glColor3f(0.0, 1.0, 1.0)  # Teal color
    points = midpoint_line(btn_l_pos[0] + btn_size, btn_l_pos[1],
                           btn_l_pos[0] - btn_size, btn_l_pos[1])
    points = points + midpoint_line(btn_l_pos[0] - btn_size, btn_l_pos[1],
                            btn_l_pos[0], btn_l_pos[1] + btn_size)
    points = points + midpoint_line(btn_l_pos[0] - btn_size, btn_l_pos[1],
                            btn_l_pos[0], btn_l_pos[1] - btn_size)
    glBegin(GL_POINTS)
    for x, y in points:
        glVertex2f(x, y)
    glEnd()


# Cross (Exit) Button
def cross_button():
    glColor3f(1.0, 0.0, 0.0)  # Red color
    points = midpoint_line(btn_r_pos[0] - btn_size// 2, btn_r_pos[1] - btn_size // 2,
                           btn_r_pos[0] + btn_size // 2, btn_r_pos[1] + btn_size // 2)
    points = points + midpoint_line(btn_r_pos[0] - btn_size // 2, btn_r_pos[1] + btn_size // 2,
                            btn_r_pos[0] + btn_size // 2, btn_r_pos[1] - btn_size // 2)
    glBegin(GL_POINTS)
    for x, y in points:
        glVertex2f(x, y)
    glEnd()



# Play/Pause Button
def play_pause_button():
    glColor3f(1.0, 0.64, 0.0)  # Amber color
    if game_paused:
        #(triangle)
        points = midpoint_line(btn_mid_pos[0] - btn_size // 2, btn_mid_pos[1] - btn_size // 2,
                               btn_mid_pos[0] + btn_size// 2, btn_mid_pos[1])
        points = points + midpoint_line(btn_mid_pos[0] - btn_size // 2, btn_mid_pos[1] + btn_size// 2,
                                btn_mid_pos[0] + btn_size // 2, btn_mid_pos[1])
    else:
        # (vertical lines)
        points = midpoint_line(btn_mid_pos[0] - btn_size// 2, btn_mid_pos[1] - btn_size// 2,
                               btn_mid_pos[0] - btn_size // 2, btn_mid_pos[1] + btn_size // 2)
        points = points + midpoint_line(btn_mid_pos[0] + btn_size // 4, btn_mid_pos[1] - btn_size // 2,
                                btn_mid_pos[0] + btn_size// 4, btn_mid_pos[1] + btn_size // 2)
    glBegin(GL_POINTS)
    for x, y in points:
        glVertex2f(x, y)
    glEnd()



def midpoint_circle(x_cntr, y_cntr, radius):
    points = []
    x = 0
    y = radius
    n = 1 - radius

    def circle_pts(x_cntr, y_cntr, x, y):
        points.extend([(x_cntr + x, y_cntr + y), (x_cntr - x, y_cntr + y),
                       (x_cntr + x, y_cntr - y), (x_cntr - x, y_cntr - y),
                       (x_cntr + y, y_cntr + x), (x_cntr - y, y_cntr + x),
                       (x_cntr + y, y_cntr - x), (x_cntr - y, y_cntr - x)])

    circle_pts(x_cntr, y_cntr, x, y)

    while x < y:
        x += 1
        if n < 0:
            n = (n + 2*x + 1)
        
        else:
            y -= 1
            n += 2 * (x - y) + 1
        circle_pts(x_cntr, y_cntr, x, y)

    return points

def drawing_circle(x_cntr, y_cntr, radius):
    glBegin(GL_POINTS)
    for (x, y) in midpoint_circle(x_cntr, y_cntr, radius):
        glVertex2f(x, y)
    glEnd()

def draw_dart(dart):
    glColor3f(1.0, 1.0, 0.0)
    drawing_circle(dart[0], dart[1], dart_radius)

def draw_shooter():
    glColor3f(0.0, 0.0, 1.0)
    drawing_circle(shooter_x, shooter_radius, shooter_radius)

def drawing_falling_circle(circle):
    glColor3f(0.0, 1.0, 0.0)
    drawing_circle(circle[0], circle[1], circle[2])

def check_collision(circle, dart):
    dy = circle[1] - dart[1]
    dx = circle[0] - dart[0] 
    distance = (dx ** 2 + dy ** 2) ** 0.5
    return distance < (circle[2] + dart_radius)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_shooter()
    for dart in darts:
        draw_dart(dart)

    for circle in falling_circles:
        drawing_falling_circle(circle)
    
    # Draw buttons
    left_arrow()
    play_pause_button()
    cross_button()

    glutSwapBuffers()


def animate():
    global darts, falling_circles, missed_circles, score, game_over

    if not game_paused and not game_over:
        new_fall_circles = []
        darts = [(x, y + dart_speed) for x, y in darts if y < W_Height]
        
        for circle in falling_circles:
            tmp_v = circle[1] - falling_speed
            if tmp_v <= 0:
                missed_circles += 1
                print("Missed Circles:", missed_circles)
                if missed_circles >= 3:
                    game_over = True
                    print("Game Over! Final Score:", score)
                    return
            else:
                new_fall_circles.append((circle[0], tmp_v, circle[2]))  # Maintain radius

        falling_circles = new_fall_circles

       
        for circle in falling_circles:
            if check_collision(circle, (shooter_x, shooter_radius)):
                game_over = True
                print("Game Over! A circle hit the shooter! Final Score:", score)
                return
        
        # collisions with darts
        for dart in darts:
            for circle in falling_circles:
                if check_collision(circle, dart):
                    darts.remove(dart)
                    falling_circles.remove(circle)
                    score += 1
                    print("Score:", score)
                    break
   
        # Spawn falling circle 
        if random.random() < 0.02:  # probability for spawning circles
            random_radius = random.randint(20, 35) #random radius
            falling_circles.append((random.randint(random_radius, W_Width - random_radius), W_Height, random_radius))

    glutPostRedisplay()


def keyboard(key, x, y):
    global shooter_x, darts

    if key == b'a':
        shooter_x = max(shooter_x - shooter_speed, shooter_radius)

    if key == b'd':
        shooter_x = min(shooter_x + shooter_speed, W_Width - shooter_radius)

    if key == b' ' and not game_over:
        darts.append((shooter_x, shooter_radius + shooter_radius))

def mouse(button, state, x, y):
    global game_paused, game_over, missed_circles, score, falling_speed, falling_circles, darts

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = W_Height - y  

        # Check Restart Button
        if check_click(x, y, btn_l_pos):
            print("Starting Over")
            score = 0
            missed_circles = 0
            game_over = False
            game_paused = False
            darts = []
            falling_circles = []
            #falling_speed = 2

        # Check Play/Pause Button
        elif check_click(x, y, btn_mid_pos):
            game_paused = not game_paused

        # Check Cross/Exit Button
        elif check_click(x, y, btn_r_pos):
            print(f"Goodbye! Final Score: {score}")
            glutLeaveMainLoop() #terminates



def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, W_Width, 0, W_Height)

glutInit()
glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
glutInitWindowSize(W_Width, W_Height)
glutCreateWindow(b"Shoot The Circles!")
glutIdleFunc(animate)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
init()
glutMainLoop()
