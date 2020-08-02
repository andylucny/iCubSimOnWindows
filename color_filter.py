import yarp
import numpy as np
import cv2
from iCubSim import iCubLimb
from iCubSim import iCubCamera
yarp.Network.init()

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
    bgr[indices[0],indices[1],:] = [255,255,0]
    # if pixel number of ball is too small, it is perhaps not the ball at all
    if np.shape(indices)[1] < 500:
        # ball not found
        return None
    else:
        # return average of x and y coordinates of blue pixels
        return (int(np.average(indices[1])),int(np.average(indices[0])))

def inverse_kinematics(position):
    positions = np.array([(245, 141), (232, 140), (500,500), (222, 134)]) # positions on image for ball position 0, 1, 2, 3 (could be extended)
    hits = np.array([(-31,0,0,50,0),(-29,17,0,49,0),(0,40,26,76,-14),(45,24,74,49,-18)],np.double) # hand position for hitting ball on position 0, 1, 2, 3 (could be extended)
    distances = np.linalg.norm(positions - position,axis=1)
    ballpos = np.argmin(distances,axis=0)
    confidence = distances[ballpos]
    #print('inverse',ballpos,confidence)
    if ballpos >= len(positions) or confidence > 4.0: # strange constant, isn't it?
        return None
    else:
        return tuple(hits[ballpos])
    
# initialize sensors and actuators
app = '/color_filter'
right_camera = iCubCamera(app,'/icubSim/cam/right')
right_arm = iCubLimb(app,'/icubSim/right_arm')
# set the right hand to the standard position
state = 0
standard_hand_position = (0,80,0,50,0,0,0,59,20,20,20,10,10,10,10,10)
right_arm.set(standard_hand_position)
# process images
while True:
    right_image = right_camera.grab()
    ball_position = blue_filter(right_image)
    if ball_position != None:
        print(ball_position)
        if state == 0:
            # if the ball is seen, hand is in the standard position and robot knows how to hit it, hit the ball!
            hand_position = inverse_kinematics(ball_position)
            if hand_position != None:
                print(hand_position)
                right_arm.set(hand_position)
                state = 1
    else:
        print('not seen')
        if state == 1:
            # if the ball is not seen and hand is not in the standard position, put hand to the standard position!
            right_arm.set(standard_hand_position)
            state = 0
    cv2.imshow('right image',right_image)
    key = cv2.waitKey(10)
    #print(key)
    if key == ord('s'):
        # if s is pressed, save image to hard disk
        cv2.imwrite('image.png',right_image)
    elif key == 27:
        # if Esc is pressed, exit
        break;

