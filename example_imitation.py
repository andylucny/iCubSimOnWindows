import numpy as np 
import cv2
import dlib
from pyicubsim import iCubLimb

head = iCubLimb('/imitation','/icubSim/head')

print('loading HOG detector')
HOG_detector = dlib.get_frontal_face_detector()

print('loading cascade regressor for landmark detection')
landmarkDetector = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        
camera = cv2.VideoCapture(0)
while True:
    hasFrame, frame = camera.read()
    if not hasFrame:
        break

    # Converting to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detection 
    faces = HOG_detector(gray,0)
    if len(faces) > 0:

        # find most central face
        faceImage = None
        min_distance = 1e9
        for face in faces:
            tl = (face.left(),face.top()) # top left point
            br = (face.right(),face.bottom()) # bottom right point
            keypoint = np.add(tl,br)//2
            centre = (frame.shape[1],frame.shape[0])
            distance = np.linalg.norm(np.subtract(centre,keypoint))
            if distance < min_distance:
                min_distance = distance
                # crop the face from the image
                faceOfs = (tl[0],tl[1])
                faceImage = gray[tl[1]:br[1],tl[0]:br[0]]
        
        if faceImage is not None and faceImage.shape[0] > 0 and faceImage.shape[1] > 0:
            # apply detector on gray face image (on the whole image)
            rect = dlib.rectangle(0,0,faceImage.shape[1],faceImage.shape[0])
            landmarks = landmarkDetector(faceImage, rect)
            if len(landmarks.parts()) == 68:
                for p in landmarks.parts():
                    cv2.circle(frame, (faceOfs[0]+p.x,faceOfs[1]+p.y), 2, (0,0,255), -1)
                p = landmarks.parts()[36] # left eye
                q = landmarks.parts()[45] # right eye
                v = dlib.point(p.x-q.x,p.y-q.y)
                u = dlib.point(v.y,-v.x)
                angle = np.arctan2(u.y,u.x)
                angle = 180*angle/np.pi
                angle -= 90
                angle = -angle
                print('angle',angle)
                # set iCub's body with the body model seen
                head.set((0,angle,0,0,0,0))
    
    cv2.imshow('camera',frame)
    if cv2.waitKey(1) == 27:
        break
        
cv2.destroyAllWindows()
