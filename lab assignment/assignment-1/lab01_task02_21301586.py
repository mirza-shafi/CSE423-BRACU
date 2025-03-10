from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random



def draw_dots():
    global blink_mode, blink_start_time, pause_mode
    glEnable(GL_POINT_SMOOTH)
    glPointSize(dot_diameter)
    glBegin(GL_POINTS)

    for i in range(len(dots)):
        x, y, color, move_x, move_y = dots[i]
        if pause_mode:
            move_x = 0
            move_y = 0
            blink_mode = False
        if blink_mode and not pause_mode:
            current_time = glutGet(GLUT_ELAPSED_TIME)
            time_diff = (current_time - blink_start_time) % 800
            if time_diff < 100:
                color = (0.0, 0.0, 0.0)
            else:
                original_color = initial_colors[i]
                color = original_color
        glColor3f(*color)
        glVertex2f(x, y)
        x += movement_speed * move_x
        y += movement_speed * move_y
        if x < boundary_left + dot_diameter:
            x = boundary_left + dot_diameter
            move_x = -move_x
        if x > boundary_right - dot_diameter:
            x = boundary_right - dot_diameter
            move_x = -move_x
        if y < boundary_bottom + dot_diameter:
            y = boundary_bottom + dot_diameter
            move_y = -move_y
        if y > boundary_top - dot_diameter:
            y = boundary_top - dot_diameter
            move_y = -move_y
        dots[i] = (x, y, color, move_x, move_y)
    glEnd()
def generate_random_dot(x, y):
    if boundary_left < x < boundary_right and boundary_bottom < y < boundary_top:
        r, g, b = (random.random(), random.random(), random.random())
        color = (r, g, b)
        move_x = random.choice([-1, 1])
        move_y = random.choice([-1, 1])
        for existing_dot in dots:
            if (
                abs(existing_dot[0] - x) < dot_diameter * 4
                and abs(existing_dot[1] - y) < dot_diameter * 4
            ):
                return
        dots.append((x, y, color, move_x, move_y))
        initial_colors.append(color)

def mouse_event(button, state, x, y):
    global blink_mode, blink_start_time, pause_mode

    if pause_mode:
        return
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        generate_random_dot(x, 600 - y)
        print("New dot added")
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if blink_mode == False:
            blink_mode = not blink_mode
            blink_start_time = glutGet(GLUT_ELAPSED_TIME)
            print("blink mode activated")
        else:
            blink_mode = not blink_mode
            print("blink mode deactivated")

def special_keys_event(key, x, y):
    global movement_speed, blink_mode, pause_mode
    if key == GLUT_KEY_UP:
        movement_speed += 0.07
        print("Speed increased")
    elif key == GLUT_KEY_DOWN:
        if movement_speed <= 0:
            movement_speed = 0
            print("speed reached")
        else:
            movement_speed -= 0.07
            print("Speed decreased")

def keyboard_event(key, x, y):
    global pause_mode, movement_speed, blink_mode, blink_mode_prev
    if key == b" ":
        pause_mode = not pause_mode
        if pause_mode:
            blink_mode_prev = blink_mode
            blink_mode = False
            for i in range(len(dots)):
                x, y, color, move_x, move_y = dots[i]
                move_x = 0
                move_y = 0
                dots[i] = (x, y, color, move_x, move_y)
            print("Dots frozen")
        else:
            blink_mode = blink_mode_prev
            blink_mode_prev = None
            for i in range(len(dots)):
                move_x = random.choice([-1, 1])
                move_y = random.choice([-1, 1])
                dots[i] = (dots[i][0], dots[i][1], dots[i][2], move_x, move_y)
            print("Dots unfrozen")
def draw_boundary():
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(boundary_right, boundary_top)
    glVertex2f(boundary_left, boundary_top)
    glVertex2f(boundary_left, boundary_top)
    glVertex2f(boundary_left, boundary_bottom)
    glVertex2f(boundary_right, boundary_bottom)
    glVertex2f(boundary_left, boundary_bottom)
    glVertex2f(boundary_right, boundary_bottom)
    glVertex2f(boundary_right, boundary_top)
    glEnd()
def setup_view():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 800, 0, 600, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    setup_view()
    glColor3f(1.0, 1.0, 1.0)
    draw_boundary()
    draw_dots()
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Point Simulation")
    glutDisplayFunc(display)
    glutMouseFunc(mouse_event)
    glutSpecialFunc(special_keys_event)
    glutKeyboardFunc(keyboard_event)
    glutIdleFunc(display)
    glutMainLoop()

# Variables
dots = []
boundary_left = 0
boundary_right = 800
boundary_bottom = 0
boundary_top = 600
dot_diameter = 15
movement_speed = 0.05
blink_mode = False
blink_mode_prev = None
blink_start_time = 0
pause_mode = False
initial_colors = []
if __name__ == "__main__":
    main()
