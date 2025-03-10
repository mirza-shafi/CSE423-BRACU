from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Window dimensions
W_Width, W_Height = 200, 600

# Game variables
score = 0

# Diamond position and color
diamond_offset_x = random.randrange(-200, 200, 10)
diamond_offset_y = 0
diamond_color = [random.random(), random.random(), random.random()]

# Catcher position and color
catcher_offset_x = 0
catcher_color = [1, 1, 1]

# Game status and speed
status = "playing"  # or "paused"
speed = 0
catch_count = 0


def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 400, 0, 600, 0, 1)
    glMatrixMode(GL_MODELVIEW)


def drawPixel(x, y):
    glPointSize(1)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()
    glFlush()


def draw8way(x, y, slope):
    draw_modes = [
        (x, y),
        (y, x),
        (-y, x),
        (-x, y),
        (-x, -y),
        (-y, -x),
        (y, -x),
        (x, -y)
    ]
    drawPixel(*draw_modes[slope])


def MidpointLine(x0, y0, x1, y1, slope):
    dx, dy = x1 - x0, y1 - y0
    delE, delNE = 2 * dy, 2 * (dy - dx)
    d = 2 * dy - dx
    x, y = x0, y0
    while x < x1:
        draw8way(x, y, slope)
        if d < 0:
            d += delE
            x += 1
        else:
            d += delNE
            x += 1
            y += 1


def drawLine(x0, y0, x1, y1):
    dx, dy = x1 - x0, y1 - y0
    if abs(dx) >= abs(dy):  # zones 0, 3, 4, and 7
        if dx >= 0:
            if dy >= 0:
                MidpointLine(x0, y0, x1, y1, 0)
            else:
                MidpointLine(x0, y0, -x1, -y1, 7)
        else:
            if dy >= 0:
                MidpointLine(-x0, y0, -x1, y1, 3)
            else:
                MidpointLine(-x0, -y0, -x1, -y1, 4)
    else:  # zones 1, 2, 5, and 6
        if dx >= 0:
            if dy >= 0:
                MidpointLine(y0, x0, y1, x1, 1)
            else:
                MidpointLine(-y0, x0, -y1, x1, 6)
        else:
            if dy >= 0:
                MidpointLine(y0, -x0, y1, -x1, 2)
            else:
                MidpointLine(-y0, -x0, -y1, -x1, 5)


def diamond():
    global diamond_offset_x, diamond_offset_y, diamond_color
    glColor3f(*diamond_color)
    drawLine(200 + diamond_offset_x, 560 + diamond_offset_y, 190 + diamond_offset_x, 540 + diamond_offset_y)
    drawLine(190 + diamond_offset_x, 540 + diamond_offset_y, 200 + diamond_offset_x, 520 + diamond_offset_y)
    drawLine(200 + diamond_offset_x, 520 + diamond_offset_y, 210 + diamond_offset_x, 540 + diamond_offset_y)
    drawLine(210 + diamond_offset_x, 540 + diamond_offset_y, 200 + diamond_offset_x, 560 + diamond_offset_y)


def catcher():
    global catcher_offset_x, catcher_color
    glColor3f(*catcher_color)
    drawLine(140 + catcher_offset_x, 30, 260 + catcher_offset_x, 30)
    drawLine(260 + catcher_offset_x, 30, 250 + catcher_offset_x, 3)
    drawLine(250 + catcher_offset_x, 3, 150 + catcher_offset_x, 3)
    drawLine(150 + catcher_offset_x, 3, 140 + catcher_offset_x, 30)


def backbtn():
    glColor3f(0.0465, 0.930, 0.724)
    drawLine(10, 580, 50, 580)
    drawLine(30, 560, 10, 580)
    drawLine(10, 580, 30, 600)


def cross():
    glColor3f(1, 0, 0)
    drawLine(390, 600, 350, 560)
    drawLine(390, 560, 350, 600)


def pausebtn():
    glColor3f(0.980, 0.765, 0.0588)
    drawLine(190, 600, 190, 560)
    drawLine(210, 560, 210, 600)


def playbtn():
    glColor3f(0.980, 0.765, 0.0588)
    drawLine(210, 580, 190, 600)
    drawLine(190, 560, 210, 580)
    drawLine(190, 600, 190, 560)


def specialKeyListener(key, x, y):
    global catcher_offset_x, status
    if status == "playing":
        if key == GLUT_KEY_LEFT and catcher_offset_x > -140:
            catcher_offset_x -= 25
        elif key == GLUT_KEY_RIGHT and catcher_offset_x < 140:
            catcher_offset_x += 25

    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global status, diamond_offset_y, score, diamond_offset_x, catcher_offset_x, catcher_color, diamond_color, speed, catch_count
    y = W_Height - y

    if 180 < x < 220 and 540 < y < 600 and button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        status = "paused" if status == "playing" else "playing"
        if status == "playing" and diamond_offset_y == 0:
            diamond_color = [random.random(), random.random(), random.random()]

    if 0 < x < 55 and 540 < y < 600 and button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        print('Starting Over')
        status = "playing"
        diamond_offset_x = random.randrange(-190, 190, 10)
        diamond_offset_y = 0
        catcher_offset_x = 0
        score = 0
        speed = 0
        catch_count = 0

    if 330 < x < 400 and 540 < y < 600 and button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        print("Goodbye :(")
        print("Final Score:", score)
        glutDestroyWindow(wind)

    glutPostRedisplay()


def animate():
    global diamond_offset_y, speed, catch_count
    if status == "playing" and diamond_offset_y > -560:
        diamond_offset_y -= (speed + 10)


def collision_check():
    global status, diamond_offset_x, diamond_offset_y, catcher_offset_x, score, diamond_color, catcher_color, catch_count, speed
    catcher_leftx = 140 + catcher_offset_x
    catcher_rightx = 260 + catcher_offset_x
    diamond_leftx = 190 + diamond_offset_x
    diamond_rightx = 210 + diamond_offset_x
    diamond_bottomy = 520 + diamond_offset_y

    if status == "playing":
        pausebtn()
        if diamond_bottomy <= 30:
            if diamond_leftx >= catcher_rightx or diamond_rightx <= catcher_leftx:
                print("Game Over! Final Score:", score)
                status = "paused"
                reset_game()
            else:
                reset_diamond()

    else:
        playbtn()


def reset_diamond():
    global diamond_offset_y, diamond_offset_x, score, diamond_color, catch_count, speed
    diamond_offset_y = 0
    diamond_offset_x = random.randrange(-190, 190, 10)
    score += 1
    diamond_color = [random.random(), random.random(), random.random()]
    print("Score:", score)
    catch_count += 1
    if catch_count == 2:
        speed += 4
        catch_count = 0


def reset_game():
    global diamond_offset_x, diamond_offset_y, catcher_offset_x, score, speed, catch_count, diamond_color, catcher_color
    diamond_offset_x = random.randrange(-190, 190, 10)
    diamond_offset_y = 0
    catcher_offset_x = 0
    score = 0
    speed = 0
    catch_count = 0
    diamond_color = [random.random(), random.random(), random.random()]
    catcher_color = [1, 1, 1]
    print("Game Reset! Ready to play.")


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Draw the catcher, diamond, and interface
    catcher()
    backbtn()
    cross()
    diamond()

    # Handle animations and collisions
    animate()
    collision_check()

    glutSwapBuffers()
    glutPostRedisplay()


# Set up OpenGL, GLUT, and the window
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(400, 600)
wind = glutCreateWindow(b"Game")

# Initialize game
init()

# Set up display and input functions
glutDisplayFunc(display)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glEnable(GL_DEPTH_TEST)

# Enter the main event loop
glutMainLoop()
