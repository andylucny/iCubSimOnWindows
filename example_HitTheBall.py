# student project, Michal Kovac, Comenius University in Bratislava, 2020
# course Introduction to Robotics, www.agentspace.org/kv
import yarp
import numpy as np
import cv2
from pyicubsim import iCubLimb, iCubCamera
import time
import threading
import os

app = '/HitTheBall'

# Based on the lesson 2
def blue_filter(bgr):
    # converting from BGR to HSV color space
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    # Hue range for blue derived from its BGR
    blue = np.uint8([[[80, 0, 0]]])
    hsvBlue = cv2.cvtColor(blue,cv2.COLOR_BGR2HSV)
    lowerLimit = np.array([hsvBlue[0][0][0]-10,100,25],np.uint8)
    upperLimit = np.array([hsvBlue[0][0][0]+10,255,255],np.uint8)
    # filtering in HSV
    mask = cv2.inRange(hsv, lowerLimit, upperLimit)
    # redraw the detected ball
    indices = np.where(mask > 0)
    #bgr[indices[0],indices[1],:] = [255,255,0]
    # if pixel number of ball is too small, it is perhaps not the ball at all
    if np.shape(indices)[1] < 500:
        # ball not found
        return None
    else:
        # return average of x and y coordinates of blue pixels
        return (int(np.average(indices[1])),int(np.average(indices[0])))

# Based on the renew script
def reset_robot_position():
    head = iCubLimb(app,'/icubSim/head')
    head.set((-40,0,0,0,0,0))

    torso = iCubLimb(app,'/icubSim/torso')
    torso.set((0,0,0))

    left_arm = iCubLimb(app,'/icubSim/left_arm')
    left_arm.set((0,80,0,50,0,0,0,59,20,20,20,10,10,10,10,10))

    right_arm = iCubLimb(app,'/icubSim/right_arm')
    right_arm.set((0,80,0,50,0,0,0,59,20,20,20,10,10,10,10,10))

    left_leg = iCubLimb(app,'/icubSim/left_leg')
    left_leg.set((0,0,0,0,0,0))

    right_leg = iCubLimb(app,'/icubSim/right_leg')
    right_leg.set((0,0,0,0,0,0))

# look for a ball and hit it
def follow_the_ball():
    reset_robot_position()

    left_camera = iCubCamera(app,'/icubSim/cam/left')
    head = iCubLimb(app,'/icubSim/head')
    torso = iCubLimb(app,'/icubSim/torso')
    right_arm = iCubLimb(app,'/icubSim/right_arm')

    left_checked = False

    while True:
        time.sleep(0.05) # prevent the system from being overloaded
        right_arm.set((0,80,0,50,0,0,0,59,20,20,20,10,10,10,10,10))
        left_image = left_camera.grab()
        ball_position = blue_filter(left_image)
        torso_position = torso.get()
        
        if ball_position != None:
            print("Ball seen on coordinates {}!".format(ball_position))

            # Move so the ball is in the correct position in the fov
            if ball_position[1] > 122:
                torso.set(joint2 = torso_position[2] + 1)
            elif ball_position[1] < 118:
                torso.set(joint2 = torso_position[2] - 1)
            elif ball_position[0] > 262:
                torso.set(joint0 = torso_position[0] + 1)
            elif ball_position[0] < 258 and torso_position[0] > -49:
                torso.set(joint0 = torso_position[0] - 1)
            else:
                # Hit the ball!
                print("Ready to hit!")
                if torso_position[0] < -49 :
                    print("Max joint position reached, the ball may be out of reach")
                     
                right_arm.set((-38,0,0,50,0,0,0,59,20,20,20,10,10,10,10,10))
                time.sleep(0.3)
            
        else:
            print('Cannot see the ball, looking for it...')
            # Move torso to look around, until the ball is found
            if torso_position[2] < 15:
                torso.set(joint2 = torso_position[2] + 1)
            elif not left_checked:
                if torso_position[0] > -30:
                    torso.set(joint0 = torso_position[0] - 1)
                else:
                    left_checked = True
            elif torso_position[0] < 30:
                torso.set(joint0 = torso_position[0] + 1)
            else:
                print("Looked everywhere, ball not found.")
                left_checked = False

def display_first_person_view():
    right_camera = iCubCamera(app,'/icubSim/cam/right')
    while True:
        right_image = right_camera.grab()
        cv2.imshow('right image',right_image)
        key = cv2.waitKey(10)
        #print(key)
        if key == ord('s'):
            # if s is pressed, save image to hard disk
            print("Saving screen capture to hard drive...")
            cv2.imwrite('image.png',right_image)
        elif key == 27:
            # if Esc is pressed, exit
            os._exit(0)

gui = threading.Thread(target=display_first_person_view)
robot_control = threading.Thread(target=follow_the_ball)

gui.start()
robot_control.start()
