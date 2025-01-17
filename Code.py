## Machine Learning Code Driver Drowsiness Detection in Python.

#driver drowsiness detection system using python, opencv, dlib

#importing required libraries
import cv2
#numpy for array related functins
import numpy as np

import dlib

#face utils for basic operations of conversion
from imutils import face_utils

#initialize the camera and taking the instance
cap = cv2.VideoCapture(0)

#initializing the face detector and landmark detector
  
detector = dlib.get_frontal_face_detector()

predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#status marking for current state
sleep = 0
drowsy = 0
active = 0
status = ""
color = (0,0,0)

#defining function in python
def compute( ptA, ptB ):
    dist = np.linalg.norm(ptA - ptB)
    return dist
 
def blinked(a, b, c, d, e, f):
    up = compute(b,d) + compute(c,e)
    down = compute(a,f)
    ratio = up/(2.0*down)

#checking if it is blinked with predefined values
    if( ratio > 0.25 ):
        return 2
    elif( ratio > 0.21 and ratio <= 0.25 ):
        return 1
    else:
        return 0


while True:
    frame = cap.read()
    #converting image to greyscale
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    faces = detector(gray)

    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        face_frame = frame.copy()
        cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        landmarks = predictor(gray,face)
        landmarks = face_utils.shape_to_np(landmarks)

        #numbers are actually the landmarks which will show eye
        left_blink = blinked(landmarks[36], landmarks[37], landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_blink = blinked(landmarks[42], landmarks[43], landmarks[44], landmarks[47], landmarks[46], landmarks[45])
          
         #now judge what to do for the eye blinks
        if( left_blink == 0 or right_blink == 0 ):
            sleep +=  1
            drowsy = 0
            active = 0
            if( sleep > 6 ):
                status = "SLEEPING !!!"
                color = (255, 0, 0)

        elif( left_blink == 1 or right_blink == 1):
            sleep = 0
            active = 0
            drowsy += 1
            if( drowsy > 6 ):
                status = "Drowsy !!"
                color = (0, 0, 255)
        else:
            drowsy = 0
            sleep = 0
            active += 1
            if( active > 6 ):
                status = "active :)"
                color = (0, 255, 0)

        cv2.putText(frame, status, (100, 100), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.2, color, 3)
        for n in range(0, 68):
            (x, y) = landmarks[n]
            cv2.circle(face_frame, (x, y), 1, (0, 255, 0), -1)
            
    cv2.imshow("frame", frame)
    cv2.imshow("Result of detector", face_frame)
    key = cv2.waitKey(1)
    if (key==27):
        break


         

 
