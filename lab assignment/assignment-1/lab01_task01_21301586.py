from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
def draw_line(x1, y1, x2, y2, width=5):
    glLineWidth(width)
    glBegin(GL_LINES)
    glVertex2f(x1,y1)
    glVertex2f(x2,y2)
    glEnd()

def draw_point(x, y, point_size=5.0):
    glPointSize(point_size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def setup_viewport():
    glViewport(0, 0, 800, 800)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 800, 0.0, 800, 0.0, 1.0) #Defines a 2D orthographic projection matrix.
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()   #Replaces the current matrix with the identity matrix.

def is_inside_house(x, y):
    return house_x_left <= x <= house_x_right and house_y_bottom <= y<= house_y_top

def update_raindrops(value):
    global raindrop_positions, wind_offset
    for i in range(10):
        x = random.randint(0, 800)
        y = random.randint(0, 800)
        while is_inside_house(x, y):
            x = random.randint(0, 800)
            y = random.randint(0, 800)
        raindrop_positions.append((x, y))

    updated_raindrops = []
    for x, y in raindrop_positions:
        y -= random.uniform(5, 25)
        if wind_offset == -1:
            x -= random.uniform(2, 5)
        elif wind_offset == 1:
            x += random.uniform(2, 5)
        if not is_inside_house(x, y):
            updated_raindrops.append((x, y))

    raindrop_positions[:] = updated_raindrops

    glutPostRedisplay()
    glutTimerFunc(30, update_raindrops, 0)

def render_scene():
    glClearColor(*background_day_color, 1.0)  #Sets the clear color for the window.
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) #Clears the window to the preset clear color.
    glLoadIdentity()
    setup_viewport()
    glColor3f(*house_color_day)  #Sets the current color for drawing.

    # base
    draw_line(house_x_left, house_y_bottom, house_x_right, house_y_bottom, width=10)
    draw_line(house_x_left, house_y_bottom, house_x_left, house_y_top, width=10)
    draw_line(house_x_right, house_y_bottom, house_x_right, house_y_top, width=10)
    draw_line(house_x_left, house_y_top, house_x_right, house_y_top, width=10)

    # roof
    roof_peak_x = (house_x_left + house_x_right) / 2
    roof_peak_y = house_y_top + 100
    draw_line(house_x_left, house_y_top, roof_peak_x, roof_peak_y, width=10)
    draw_line(house_x_right, house_y_top, roof_peak_x, roof_peak_y, width=10)

    # window
    window_x_left = house_x_left + 50
    window_x_right = window_x_left + 50
    window_y_bottom = house_y_bottom + 100
    window_y_top = window_y_bottom + 50
    draw_line(window_x_left, window_y_bottom, window_x_right, window_y_bottom, width=6)
    draw_line(window_x_left, window_y_bottom, window_x_left, window_y_top, width=6)
    draw_line(window_x_right, window_y_bottom, window_x_right, window_y_top, width=6)
    draw_line(window_x_left, window_y_top, window_x_right, window_y_top, width=6)

    # window_design
    draw_line((window_x_left + window_x_right) / 2, window_y_bottom, (window_x_left + window_x_right) / 2, window_y_top,
              width=4)
    draw_line(window_x_left, (window_y_bottom + window_y_top) / 2, window_x_right, (window_y_bottom + window_y_top) / 2,
              width=4)

    # door
    door_x_left = house_x_right - 100
    door_x_right = door_x_left + 50
    door_y_bottom = house_y_bottom
    door_y_top = door_y_bottom + 120
    draw_line(door_x_left, door_y_bottom, door_x_left, door_y_top, width=10)
    draw_line(door_x_right, door_y_bottom, door_x_right, door_y_top, width=10)
    draw_line(door_x_left, door_y_top, door_x_right, door_y_top, width=10)

    # doorknob
    draw_point(door_x_right - 10, door_y_bottom + 60, point_size=8.0)

    # raindrops
    glColor3f(0.0, 0.0, 1.0)  # Raindrop color (blue)
    for x, y in raindrop_positions:
        draw_line(x, y, x, y - 10, width=2)

    glutSwapBuffers()

def handle_key_press(key, x, y):
    global background_day_color, house_color_day, wind_offset
    if key == b'd':
        background_day_color = (1.0, 1.0, 1.0)
        house_color_day = (0.0, 0.0, 0.0)
    elif key == b'n':
        background_day_color = (0.0, 0.0, 0.0)
        house_color_day = (1.0, 1.0, 1.0)
    elif key == b' ':
        wind_offset = 0
    elif key == b'\x1b':
        glutLeaveMainLoop()
    glutPostRedisplay()
def handle_special_key_press(key, x, y):
    global wind_offset
    if key == GLUT_KEY_LEFT:
        wind_offset = -1
    elif key == GLUT_KEY_RIGHT:
        wind_offset = 1
    glutPostRedisplay()

raindrop_positions = []
background_day_color = (1.0, 1.0, 1.0)
background_night_color = (0.0, 0.0, 0.0)
house_color_day = (0.0, 0.0, 0.0)
house_color_night = (1.0, 1.0, 1.0)
house_x_left = 200
house_x_right = 600
house_y_bottom = 200
house_y_top = 400
wind_offset = 0

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(800, 800)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Rain Simulation")
glutDisplayFunc(render_scene)
glutKeyboardFunc(handle_key_press)
glutSpecialFunc(handle_special_key_press)
glutTimerFunc(1, update_raindrops, 0)
glutMainLoop()
