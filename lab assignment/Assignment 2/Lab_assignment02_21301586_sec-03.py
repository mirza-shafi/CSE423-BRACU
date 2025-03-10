from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_Width, W_Height = 200, 600      # window dimensions
score = 0
diamond_offset_x = random.randrange(-200, 200, 10)
diamond_offset_y = 0
diamond_color = [random.random(), random.random(), random.random()]
catcher_offset_x = 0  # 0---> horizontal position
catcher_color = [1, 1, 1]    # white
status = "playing"  # or "paused"
speed = 0
catch_count = 0

# This function sets up the OpenGL environment with a black background and a 2D projection (used for 2D games).
def init() :
    glClearColor(0, 0, 0, 0)    # black
    glMatrixMode(GL_PROJECTION)   # Set the projection matrix mode
    glLoadIdentity()   # Reset the current matrix
    glOrtho(0, 400, 0, 600, 0, 1)  # Set an orthographic projection (2D view)
    glMatrixMode(GL_MODELVIEW)  # Switch to the modelview matrix


#  Draws a single pixel at coordinates (x, y).
def drawPixel(x, y):
    glPointSize(1)    # Set pixel size to 1
    glBegin(GL_POINTS)   # Start drawing points
    glVertex2f(x, y)     # Specify the coordinates for the pixel
    glEnd()             # End drawing
    glFlush()           # Force OpenGL to execute the drawing command immediately

#   This function draws a pixel in 8 symmetrical positions for different line zones based on slope.
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

#  This function uses the Midpoint Line Algorithm to draw a line between two points.
#  It checks if the next pixel should be placed to the east or north-east of the current pixel.
def MidpointLine(x0, y0, x1, y1, slope):
    dx, dy = x1 - x0, y1 - y0
    delE, delNE = 2 * dy, 2 * (dy - dx)    # Initialize decision factors for the algorithm
    d = 2 * dy - dx
    x, y = x0, y0      # Starting point of the line
    while x < x1:
        draw8way(x, y, slope)
        if d < 0:
            d += delE
            x += 1
        else:
            d += delNE
            x += 1
            y += 1

#This function handles lines in different zones by calling MidpointLine for the appropriate slope.
def drawLine(x0, y0, x1, y1):
    dx, dy = x1 - x0, y1 - y0
    if abs(dx) >= abs(dy):  # If the line is more horizontal (zones 0, 3, 4, and 7)
        if dx >= 0:     # Moving right
            if dy >= 0:  # Moving up
                MidpointLine(x0, y0, x1, y1, 0)
            else:       # Moving down
                MidpointLine(x0, y0, -x1, -y1, 7)
        else:
            if dy >= 0:
                MidpointLine(-x0, y0, -x1, y1, 3)
            else:
                MidpointLine(-x0, -y0, -x1, -y1, 4)
    else:  # More vertical line (zones 1, 2, 5, and 6)
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
#  Draws a diamond at its current position with four lines forming a diamond shape.
def diamond():
    global diamond_offset_x, diamond_offset_y, diamond_color
    glColor3f(*diamond_color)
    drawLine(200 + diamond_offset_x, 560 +diamond_offset_y, 190 + diamond_offset_x, 540 + diamond_offset_y)
    drawLine(190 + diamond_offset_x, 540 + diamond_offset_y, 200+ diamond_offset_x, 520 + diamond_offset_y)
    drawLine(200 + diamond_offset_x, 520 + diamond_offset_y, 210 + diamond_offset_x, 540 + diamond_offset_y)
    drawLine(210 + diamond_offset_x, 540 + diamond_offset_y, 200 + diamond_offset_x, 560 +diamond_offset_y)


# Draws the catcher (a rectangular object) at the bottom of the screen.
def catcher():
    global catcher_offset_x, catcher_color
    glColor3f(*catcher_color)
    drawLine(140 + catcher_offset_x, 30, 260 + catcher_offset_x, 30)
    drawLine(260 + catcher_offset_x, 30, 250 + catcher_offset_x, 3)
    drawLine(250 + catcher_offset_x, 3, 150 + catcher_offset_x, 3)
    drawLine(150 + catcher_offset_x, 3, 140 + catcher_offset_x, 30)

#  Draws buttons for restarting, pausing, and exiting the game.
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

#   Listens for mouse clicks on the game buttons (restart, pause, exit)
# The mouseListener function handles mouse clicks within the game.
def mouseListener(button, state, x, y):
    global status, diamond_offset_y, score, diamond_offset_x, catcher_offset_x, catcher_color, diamond_color, speed, catch_count
    y = W_Height - y    # Invert the y-coordinate to match OpenGL's bottom-left origin (screen coordinates)

#  "paused" and "playing"
    if 180 < x < 220 and 540 < y < 600 and button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        status = "paused" if status == "playing" else "playing"
        if status == "playing" and diamond_offset_y == 0:
            diamond_color = [random.random(), random.random(), random.random()]

# the game restarts.
    if 0 < x < 55 and 540 < y < 600 and button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        print('Starting Over')
        status = "playing"
        diamond_offset_x = random.randrange(-190, 190, 10)
        diamond_offset_y = 0
        catcher_offset_x = 0
        score = 0
        speed = 0
        catch_count = 0

#  the game exits.
    if 330 < x < 400 and 540 < y < 600 and button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        print("Goodbye :(")
        print("Final Score:", score)
        glutDestroyWindow(wind)

    glutPostRedisplay()

# Updates the diamond's falling position.
def animate():
    global diamond_offset_y, speed, catch_count
    if status == "playing" and diamond_offset_y > -560:
        diamond_offset_y -= (speed + 10)  # Move the diamond down

# Checks if the diamond is caught by the catcher or missed.
def collision_check():
    global status, diamond_offset_x, diamond_offset_y, catcher_offset_x, score, diamond_color, catcher_color, catch_count, speed
    catcher_leftx = 140 + catcher_offset_x
    catcher_rightx = 260 + catcher_offset_x
    diamond_leftx = 190 + diamond_offset_x
    diamond_rightx = 210 + diamond_offset_x
    diamond_bottomy = 520 + diamond_offset_y

    if status == "playing":
        pausebtn()
        if diamond_bottomy <= 30:  # If the diamond reaches the bottom
            if diamond_leftx >= catcher_rightx or diamond_rightx <= catcher_leftx:
                print("Game Over! Final Score:", score)
                status = "paused"   # Missed the diamond
                reset_game()   # Reset everything
            else:
                reset_diamond()    # Reset diamond if caught

    else:
        playbtn()


def reset_diamond():
    global diamond_offset_y, diamond_offset_x, score, diamond_color, catch_count, speed
    diamond_offset_y = 0    # Reset the diamond to the top of the screen (y position)
    diamond_offset_x = random.randrange(-190, 190, 10)  # Randomly choose a new horizontal position for the diamond
    score += 1
    diamond_color = [random.random(), random.random(), random.random()]
    print("Score:", score)
    catch_count += 1
    if catch_count == 2:  # After catching two diamonds, increase the falling speed
        speed += 4
        catch_count = 0



def reset_game():
    global diamond_offset_x, diamond_offset_y, catcher_offset_x, score, speed, catch_count, diamond_color, catcher_color
    diamond_offset_x = random.randrange(-190, 190, 10)   # Random horizontal position for the diamond
    diamond_offset_y = 0   # Reset the diamond to the top
    catcher_offset_x = 0   # Reset the catcher's position to the center of the screen
    score = 0
    speed = 0
    catch_count = 0
    diamond_color = [random.random(), random.random(), random.random()]  # New random color for the diamond
    catcher_color = [1, 1, 1]
    print("Game Reset! Ready to play.")

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    catcher()
    backbtn()
    cross()
    diamond()
    animate()
    collision_check()
    glutSwapBuffers()    # Swap the buffers for smooth display
    glutPostRedisplay()
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(400, 600)
wind = glutCreateWindow(b"Game")
init()
glutDisplayFunc(display)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glEnable(GL_DEPTH_TEST)
glutMainLoop()
