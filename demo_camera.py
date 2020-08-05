import yarp
from pyicubsim import iCubCamera
import cv2

app = '/disparity'
left_camera = iCubCamera(app,'/icubSim/cam/left')
right_camera = iCubCamera(app,'/icubSim/cam/right')

# create stereovision object
#stereo = cv2.createStereoBM(numDisparities=16, blockSize=15) # OpenCV3
stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15) # OpenCV4

while True:
    # get images from left and right camera
    left_image = left_camera.grab()
    right_image = right_camera.grab()

    # show the seen image
    image_seen = cv2.hconcat([left_image,right_image])
    cv2.imshow('image',image_seen)

    # turn color images to greyscale images
    left_image = cv2.cvtColor(left_image, cv2.COLOR_BGR2GRAY)
    right_image = cv2.cvtColor(right_image, cv2.COLOR_BGR2GRAY)

    # calculate depth map
    disparity = stereo.compute(left_image,right_image)

    # show the result
    normalized_disparity = cv2.normalize(disparity, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    normalized_disparity = 255-normalized_disparity
    cv2.imshow('disparity',normalized_disparity)
    if cv2.waitKey(10) == 27:
        break
        