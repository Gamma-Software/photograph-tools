# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
from datetime import date
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import os
import shutil


def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear

# frames the eye must be below the threshold
EYE_AR_THRESH = 0.35
EYE_AR_CONSEC_FRAMES = 3

# initialize the frame counters and the total number of blinks
COUNTER = 0
TOTAL = 0

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("data/shape_predictor_68_face_landmarks.dat")

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

time.sleep(1.0)

output_folder = 'output'+date.today().isoformat()
os.makedirs(output_folder+'/eyes_open')
os.makedirs(output_folder+'/eyes_close')

# loop over frames from the video stream
# if this is a file video stream, then we need to check if
# there any more frames left in the buffer to process

# grab the frame from the threaded video file stream, resize
# it, and convert it to grayscale
# channels)

filenames = next(os.walk("data/images/"), (None, None, []))[2]  # [] if no file

for f in filenames:
    print()
    print(f)
    frame = cv2.imread('data/images/'+f, cv2.IMREAD_GRAYSCALE)
    frame = imutils.resize(frame, width=450)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = frame

    # detect faces in the grayscale frame
    rects = detector(gray, 0)

    # loop over the face detections
    i = 0
    for rect in rects:
        i += 1
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # extract the left and right eye coordinates, then use the
        # coordinates to compute the eye aspect ratio for both eyes
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        # average the eye aspect ratio together for both eyes
        ear = (leftEAR + rightEAR)

        # compute the convex hull for the left and right eye, then
        # visualize each of the eyes
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        # check to see if the eye aspect ratio is below the blink
        # threshold, and if so, increment the blink frame counter
        if ear < EYE_AR_THRESH:
            cv2.putText(frame, "Eye: {}".format("close"), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            print('Closed')
            shutil.copy2('data/images/'+f, output_folder+'/eyes_close/'+f)


        # otherwise, the eye aspect ratio is not below the blink
        # threshold
        else:
            cv2.putText(frame, "Eye: {}".format("Open"), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            print('Opened')
            shutil.copy2('data/images/'+f, output_folder+'/eyes_open/'+f)
    print("number of people: " + str(i))

if len(os.listdir(output_folder+'/eyes_open')) == 0:
    os.removedirs(output_folder+'/eyes_open')
if len(os.listdir(output_folder+'/eyes_close')) == 0:
    os.removedirs(output_folder+'/eyes_close')