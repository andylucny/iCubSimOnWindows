import yarp
import numpy as np
import cv2

yarp.Network.init()

port_left = yarp.Port()
port_left.open('/test/cam/left')
port_right = yarp.Port()
port_right.open('/test/cam/right')
yarp.delay(0.5)
yarp.Network.connect('/icubSim/cam/left','/test/cam/left')
yarp.Network.connect('/icubSim/cam/right','/test/cam/right')
yarp.delay(0.5)

width = 320
height = 240
yarp_img_left = yarp.ImageRgb()
yarp_img_left.resize(width,height)
array_img_left = bytearray(width*height*3)
yarp_img_left.setExternal(array_img_left, width, height)
yarp_img_right = yarp.ImageRgb()
yarp_img_right.resize(width,height)
array_img_right = bytearray(width*height*3)
yarp_img_right.setExternal(array_img_right, width, height)
padding = np.zeros((240,50,3),np.uint8)

while True:
    port_left.read(yarp_img_left)
    port_right.read(yarp_img_right)
    if yarp_img_left.height() == height and yarp_img_left.width() == width and \
       yarp_img_right.height() == height and yarp_img_right.width() == width:
        img_left = np.frombuffer(array_img_left, dtype=np.uint8).reshape(height,width,3)
        img_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2RGB)
        img_right = np.frombuffer(array_img_right, dtype=np.uint8).reshape(height,width,3)
        img_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2RGB)
        img = np.concatenate((img_left, padding, img_right), axis=1)
        cv2.imshow('camera',img)
        if cv2.waitKey(10) == 27:
            break
