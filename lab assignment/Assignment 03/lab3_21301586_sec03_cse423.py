from OpenGL.GL import *
from OpenGL.GLUT import *
import random

dis = 500  #  Distance for randomizing targets.
pause = False
score = 0
gameOver = False
shoot = False

# Define the clickable areas for pause, resume, and restart buttons.
cross_area = [0,0,0,0]
pause_area =[0,0,0,0]
resume_area =[0,0,0,0]
restart_area =[0,0,0,0]
five_circles_area=[]   # Stores the boundaries of each falling circle.
#  Controls the movement of the shooter circle.
Left = 0
Right = 0
s1, s2 = 5000,500  # Initial positions of the shooter circle.
curr_x, curr_y = s1, s2
targetspeed= 10   # Speed at which target circles fall.
bulletspeed= 700
bulletlist= []
gameover= False
r,g,b= 0,1,1
five_circle_list = []
five_circle_area_list = []
circle_x = []
gone = False
clash= False
clash1= False
bothC= False
shooter_area= [0,0,0,0]  # Stores the shooter circle's area for collision detection.
bcol= []  # List storing bullet color.

# This function generates 5 circles with random vertical positions and radii.
# It places the circles horizontally apart by 1500 units starting from the value of x1.
def gen(x1):
   for x in range(5):
       y1=random.randint(6000,8000)    # Random y-coordinate for each circle.
       rad=random.randint(100,500)    # Random radius for each circle.
       five_circle_list.append([x1,y1,rad])   # Append the circle data (x, y, radius) to the list.
       five_circle_area_list.append([x1-rad,x1+rad,y1-rad,y1+rad])  # Calculate and store its bounding area.
       x1=x1+1500  # Move the next circle to the right by 1500 units.
   return
gen(2000)  # Call the function to generate 5 circles starting at x=2000.

def pauseGame():
   global pause
   if pause == False:
       pause = True
   else:
       pause = False

def draw_points(x0, y0):
   glPointSize(1)   # Set the size of the point to 1 pixel.
   glBegin(GL_POINTS)  # Start drawing points.
   glVertex2f(x0, y0)   # Draw a point at (x0, y0).
   glEnd()    # End drawing points.

def midpoint (x0, y0, x1, y1):
   zone = findZone(x0, y0, x1, y1)   # Determine which "zone" the line is in (used to handle line drawing).
   x0, y0 = zoneConvert0(zone, x0, y0)  # Convert to Zone 0 coordinates for easier calculations.
   x1, y1 = zoneConvert0(zone, x1, y1)
   dx = x1 - x0
   dy = y1 - y0
   dinit = 2 * dy - dx
   dne = 2 * dy - 2 * dx
   de = 2 * dy
   for i in range(x0, x1):    # Loop through x-coordinates.
       a, b = convert_back_from_0(zone, x0, y0)   # Convert back from Zone 0 coordinates.
       if dinit >= 0:    # If the decision parameter is positive, move diagonally.
           dinit = dinit + dne
           draw_points(a, b)   # Draw the point
           x0 += 1
           y0 += 1
       else:     # If the decision parameter is negative, move horizontally.
           dinit = dinit + de
           draw_points(a, b)
           x0 += 1
# findZone(x0, y0, x1, y1): Determines which of the 8 possible zones a line is in based on the slope.
# This helps simplify the line drawing process.
def findZone(x0, y0, x1, y1):
   dx = x1 - x0
   dy = y1 - y0
   if abs(dx) > abs(dy):
       if dx > 0 and dy > 0:
           return 0
       elif dx < 0 and dy > 0:
           return 3
       elif dx < 0 and dy < 0:
           return 4
       else:
           return 7
   else:
       if dx > 0 and dy > 0:
           return 1
       elif dx < 0 and dy > 0:
           return 2
       elif dx < 0 and dy < 0:
           return 5
       else:
           return 6

#  Converts coordinates from the current zone to Zone 0, which is the simplest for drawing lines.
def zoneConvert0(zone, x0, y0):
   if zone == 0:
       return x0, y0
   elif zone == 1:
       return y0, x0
   elif zone == 2:
       return -y0, x0
   elif zone == 3:
       return -x0, y0
   elif zone == 4:
       return -x0, -y0
   elif zone == 5:
       return -y0, -x0
   elif zone == 6:
       return -y0, x0
   elif zone == 7:
       return x0, -y0


# convert_back_from_0(): Converts coordinates from Zone 0 back to the original zone.
def convert_back_from_0(zone, x0, y0):
   if zone == 0:
       return x0, y0
   if zone == 1:
       return y0, x0
   if zone == 2:
       return y0, -x0
   if zone == 3:
       return -x0, y0
   if zone == 4:
       return -x0, -y0
   if zone == 5:
       return -y0, -x0
   if zone == 6:
       return y0, -x0
   if zone == 7:
       return x0, -y0

def specialKeyListener(key, left, right):
   glutPostRedisplay()    # Redraw the screen.
   global Left, Right, x0, x1,l1,r1,s1,s2,k1,k2,curr_y,curr_x
   if pause == False:
       if key == GLUT_KEY_LEFT :
           if s1 - Left + Right > 500:  # Move left only if not at the left edge.
               Left += 250
               curr_x=s1 - Left + Right
       elif key == GLUT_KEY_RIGHT:
           if s1 - Left + Right <= 9500:  # Move right only if not at the right edge.
               Right += 250
               curr_x=s1 - Left + Right
       glutPostRedisplay()


def keyboardListener(key, x, y):
    global Left, Right, s1, curr_x
    if key == b'a':  # Move left when 'A' is pressed
        if s1 - Left + Right > 500:
            Left += 200
            curr_x = s1 - Left + Right
    elif key == b'd':  # Move right when 'D' is pressed
        if s1 - Left + Right <= 9500:
            Right += 200
            curr_x = s1 - Left + Right
    elif key == b' ':  # Shoot when spacebar is pressed
        global shoot, bulletlist, bcol, clash1
        shoot = True
        clash1 = False
        bcol = [0, 1, 1]  # Bullet color
        bulletlist.append([curr_x, curr_y, clash1, bcol])
    glutPostRedisplay()

# iterate(): Sets up the viewing area in OpenGL.
def iterate():
   glViewport(0, 0, 500, 500)
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   glOrtho(0.0, 10000, 0.0, 10000, 0.0, 1.0)
   glMatrixMode(GL_MODELVIEW)
   glLoadIdentity()
# mouseListener(): Listens for mouse clicks and checks if any of the control buttons (pause, restart, or exit) were clicked.
# It performs appropriate actions such as restarting or pausing the game.
def mouseListener(button, state, x, y):
   global cross_area, pause_area, resume_area, restart_area,pause,five_circle_area_list
   global Left, Right,s1,s2,curr_x,curr_y,targetspeed,bulletspeed , bulletlist,score,circle_x,gone,gameOver
   global shoot,five_circle_list,five_circles_area,score,bothC,shooter_area,once,twi,countb,count
   if button == GLUT_LEFT_BUTTON:
       if (state == GLUT_DOWN):
           if restart_area[0]/20<=x<=restart_area[1]/20 and restart_area[2]/20<=500-y<=restart_area[3]/20:
               print(f"Game Restarted!! Previous Score: {score}")
               print('Restart')
               five_circles_area = []
               Left = 0
               Right = 0
               s1, s2 = 5000, 500
               curr_x, curr_y = s1, s2
               targetspeed = 20
               bulletspeed = 500
               bulletlist = []
               pause = False
               score = 0
               gameOver = False
               shoot = False
               five_circle_list = []
               five_circle_area_list = []
               circle_x = []
               gone = False
               bothC = False
               shooter_area = [0, 0, 0, 0]
               once = False
               twi = False
               countb = 0
               once = False
               twi = False
               countb = 0
               count=0
               gen(2000)
               glutPostRedisplay()
           if pause_area[0]/20<=x<=pause_area[1]/20 and pause_area[2]/20<=500-y<=pause_area[3]/20:
               pauseGame()
               glutPostRedisplay()
               print("Pause")
           if  resume_area[0]/20<=x<= resume_area[1]/20 and resume_area[2]/20<=500-y<= resume_area[3]/20:
               print("Resume")
               glutPostRedisplay()
           if  cross_area[0]/20<=x<= cross_area[1]/20 and  cross_area[2]/20<=500-y<= cross_area[3]/20:
               print("GameOver")
               print('TotalScore:',score)
               glutLeaveMainLoop()

def restart_icon():
   global restart_area
   glColor3f(1.0, 0.0, 1.0)
   midpoint(200, 9400, 500, 9700)
   midpoint(200, 9400, 500, 9100)
   midpoint(200, 9400, 800, 9400)
   restart_area[0],restart_area[1],restart_area[2],restart_area[3]=200,800,9100,9700  # Define clickable area for restart.


def cross_icon():
   global cross_area
   glColor3f(0.0, 0.0, 1.0)
   midpoint(9200, 9700, 9800, 9100)
   midpoint(9200, 9100, 9800, 9700)
   cross_area[0],cross_area[1],cross_area[2],cross_area[3]=9200,9800,9100,9700

def pause_icon():
   global pause_area
   glColor3f(1.0, 1.0, 0.0)
   midpoint(4800, 9700, 4800, 9100)
   midpoint(5200, 9700, 5200, 9100)
   pause_area[0],pause_area[1],pause_area[2],pause_area[3]=4800,5200,9100,9700

def resume():
   global resume_area
   glColor3f(1.0, 1.0, 0.0)
   midpoint(4800, 9700, 4800, 9100)
   midpoint(4800, 9100, 5400, 9400)
   midpoint(4800, 9700, 5400, 9400)
   resume_area[0], resume_area[1], resume_area[2], resume_area[3] = 4800,5400,9100,9700



def draw_circle_shooter(x_centre, y_centre, radius):
   global shooter_area,Left,Right,shoot
   glColor3f(1.0, 0.0, 0.0)
   x, y = 0, radius
   d = 1 - radius
   glBegin(GL_POINTS)
   while x <= y:     # Loop to draw points based on the Midpoint Circle Algorithm.
       glVertex2f(x + x_centre-Left+Right, y + y_centre)
       glVertex2f(-x + x_centre-Left+Right, y + y_centre)
       glVertex2f(x + x_centre-Left+Right, -y + y_centre)
       glVertex2f(-x + x_centre-Left+Right, -y + y_centre)
       glVertex2f(y + x_centre-Left+Right, x + y_centre)
       glVertex2f(-y + x_centre-Left+Right, x + y_centre)
       glVertex2f(y + x_centre-Left+Right, -x + y_centre)
       glVertex2f(-y + x_centre-Left+Right, -x + y_centre)
       if d < 0:
           d += 2 * x + 3
       else:
           d += 2 * (x - y) + 5
           y -= 1
       x += 1
   glEnd()

# Draws the falling target circles using the Midpoint Circle Algorithm, similarly to the shooter circle.
def draw_circle_target(x_centre, y_centre, radius):
   global shooter_area,Left,Right,shoot
   glColor3f(1.0, 1.0, 0.0)
   x, y = 0, radius
   d = 1 - radius   # Initial decision parameter for the midpoint algorithm.
   glBegin(GL_POINTS)
   while x <= y:
       glVertex2f(x + x_centre, y + y_centre)
       glVertex2f(-x + x_centre, y + y_centre)
       glVertex2f(x + x_centre, -y + y_centre)
       glVertex2f(-x + x_centre, -y + y_centre)
       glVertex2f(y + x_centre, x + y_centre)
       glVertex2f(-y + x_centre, x + y_centre)
       glVertex2f(y + x_centre, -x + y_centre)
       glVertex2f(-y + x_centre, -x + y_centre)
       if d < 0:
           d += 2 * x + 3
       else:
           d += 2 * (x - y) + 5
           y -= 1
       x += 1
   glEnd()


def draw_circle_bullet(x_centre, y_centre, radius,col):
   global shooter_area,Left,Right,shoot,clash1
   x, y = 0, radius
   d = 1 - radius
   r,g,b=col[0],col[1],col[2]    # Set the bullet color based on the col parameter.
   # Similar structure to the draw_circle_shooter() function.
   glColor3f(r,g,b)
   glBegin(GL_POINTS)
   while x <= y:
       glVertex2f(x + x_centre, y + y_centre)
       glVertex2f(-x + x_centre, y + y_centre)
       glVertex2f(x + x_centre, -y + y_centre)
       glVertex2f(-x + x_centre, -y + y_centre)
       glVertex2f(y + x_centre, x + y_centre)
       glVertex2f(-y + x_centre, x + y_centre)
       glVertex2f(y + x_centre, -x + y_centre)
       glVertex2f(-y + x_centre, -x + y_centre)
       if d < 0:
           d += 2 * x + 3
       else:
           d += 2 * (x - y) + 5
           y -= 1
       x += 1
   glEnd()


def animate():
   global gone,pause,gameover
   if pause==False and gameover==False:
       if gone==False:
           animatetarget()   # Move the targets down the screen.
           animateshooter()  # Move the shooter and bullets.
           glutPostRedisplay()
       else:
           pass
   else:
       pass


count=0
def animatetarget():
   global five_circle_list,targetspeed,shoot,s1,s2,k1,k2,bulletlist,bulletspeed,five_circle_area_list,five_circle_list,score,r
   global count,gone,s1,s2,Left,Right,score,bothC,shooter_area
   if count==3:  # If the player has missed 3 circles, the game is over.
       gone=True
       print("GameOver")
       print("Total Score:",score)
   else:
       for cir in range(len(five_circle_list)):
           if five_circle_list[cir]==None:
               pass
           else:
               circle_y=five_circle_list[cir][1]  # Get the current y-coordinate of the circle.
               circle_x=five_circle_list[cir][0]  # Get the current x-coordinate of the circle.
               leftx,rightx=circle_x-five_circle_list[cir][2],circle_x+five_circle_list[cir][2] # Calculate left boundary.
               if bothC==True:
                   pass
               else:
                   k=circle_y-five_circle_list[cir][2]
                   if shooter_area[2]<=k<=shooter_area[3]:  # Check if the circle has reached the shooter's area.
                       if shooter_area[0]<=leftx<=shooter_area[1] or  shooter_area[0]<=rightx<=shooter_area[1]:
                           gone=True    # End the game if the circle touches the shooter.
                           print("Gameover")
                           print("Total Score:",score)
                   if circle_y<0 :   # If the circle has reached the bottom of the screen (missed by the player).
                       count+=1
                       five_circle_list[cir]=None
                   else:
                       circle_y=(circle_y-targetspeed)
                       five_circle_list[cir][1]=circle_y  # Update the circle's y-coordinate.
once=False
twi=False
countb=0
# function is responsible for animating the bullets shot by the player. It moves the bullets upward, checks for collisions with falling circles,
# and removes bullets that leave the screen or hit a target.
def animateshooter():
   global five_circle_list,targetspeed,shoot,s1,s2,k1,k2,bulletlist,bulletspeed,five_circle_area_list,five_circle_list,score,r
   global once,dis,clash1,countb,gone
   if shoot==False:  # If no shooting is happening, do nothing.
       pass
   else:
       if countb//3 == 3:    # If the player has misfired 3 times, end the game.
           gone = True
           print("GameOver")
           print("Total Score:", score)
       else:

           for x in range(len(bulletlist)):
               if bulletlist[x]==None:
                   pass
               else:
                   b=bulletlist[x][1]  # Get the bullet's y-coordinate.
                   if 9000<=b<=10000 and bulletlist[x][3]==[0,1,1]:  # If the bullet moves beyond the top of the screen.
                       countb+=1
                   a=bulletlist[x][0]
                   if clash1==True:
                       pass
                   else:
                       b=(b+bulletspeed)
                       # Check for collisions with the falling circles.
                   for p in range(len(five_circle_area_list)):
                       # Check if the bullet is within the boundaries of the circle.
                       if five_circle_area_list[p][0]<=a<=five_circle_area_list[p][1] and five_circle_area_list[p][2]<=b<=five_circle_area_list[p][3]:
                           temp=five_circle_list[p][0]   # Store the circle's x-coordinate.
                           five_circle_list[p]=None      # Mark the circle as hit (remove it).
                           clash1=True
                           bulletlist[x][3]=[0,0,0]   # Change bullet color to black (hit).
                           if once==False:
                               k=random.randint(100,500)
                               five_circle_list[p]=[temp+dis,random.randint(6000,8000),k]
                               five_circle_area_list[p][0]=temp+dis-k
                               five_circle_area_list[p][1] = temp + dis + k
                               once=True
                           else:
                               # Generate a new circle at a different position.
                               k=random.randint(100,500)
                               five_circle_list[p]=[temp-dis,random.randint(6000,8000),k]
                               five_circle_area_list[p][0]=temp-dis - k  # Update the new circle's area.
                               five_circle_area_list[p][1] = temp - dis + k
                               once=False
                           score += 1
                           if twi==True:
                               print("Score:", score)
                           else:
                               print("Score:", score-1)
                       else:
                           bulletlist[x][1] = b

def showScreen():
   global five_circle_list, s1, s2, shoot, bulletlist, shooter_area, Left, Right
   global bcol
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the screen
   glLoadIdentity()    # Reset the transformations.
   iterate()       # Set up the viewport and projection.
   glColor3f(0.0, 0.0, 0.0)
   restart_icon()
   cross_icon()
   if pause == False:
       pause_icon()
   else:
       resume()
   draw_circle_shooter(s1, s2, 300)
   shooter_area[0],shooter_area[1],shooter_area[2],shooter_area[3]=[s1-300-Left+Right,s1+300-Left+Right,s2-300,s2+300]

   for circle in five_circle_list:
       if circle is not None and len(circle) >= 3:
           draw_circle_target(circle[0], circle[1], circle[2])
   if shoot == True:
       if len(bulletlist) == 0:
           pass
       else:
           for bullet in bulletlist:
               if bullet is not None and len(bullet) >= 2:
                   draw_circle_bullet(bullet[0], bullet[1], 50,bullet[3])
               else:
                   pass
   glutSwapBuffers()     # Swap the buffers to display the new frame

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Game")
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)
glutMainLoop()

