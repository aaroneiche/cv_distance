from pickle import FALSE
from random import getrandbits
import cv2
import numpy as np
import argparse
import imutils
import math
from enum import Enum


drawContours = False        # c - also, deprecated.
drawBlobs = False           # b
drawDistances = False       # d
drawLines = False           # l

class Mode(Enum):
    COLOR = 1
    GRAY = 2
    THRESH = 3
    DATA = 4

currentMode = Mode.DATA
# The focal length for the Logitech c910, determined emperically
# For more details, read here: https://pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/
focalLength = 2159 

# Blob Detection parameters
params = cv2.SimpleBlobDetector_Params()
params.filterByCircularity = True
params.minCircularity = 0.5
params.minArea = 200
params.maxArea = 20000

# Distance between two cartesian coordinates
def DistanceSquared(point1, point2):
    diffX = point1[0] - point2[0]
    diffY = point1[1] - point2[1]
    return (diffX*diffX+diffY*diffY)

def process_image(input, type):
    
    #Determine Type
    if type == 'video':
        cap = cv2.VideoCapture(input)
        frame_counter = 0
    elif type == 'live':
        cap = cv2.VideoCapture(0)
    else: 
        cap = cv2.imread(input)


    global currentMode
    global drawLines
    global drawDistances
    global drawBlobs
    global focalLength

    while (True):
        if type == 'video' :
            # Capture frame-by-frame
            ret, frame = cap.read()

            frame_counter += 1
            #If the last frame is reached, reset the capture and the frame_counter
            if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                frame_counter = 0 #Or whatever as long as it is the same as next line
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue #restart the loop so we're not referencing a non-existant frame
        elif type == 'live':
            ret, frame = cap.read()
        else:
            frame = cap

        # Adjust the image for better threshold values
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh_ret, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
        
        #This part of the script is depricated, left here for history's sake
        if drawContours:
            # contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = cv2.findContours(thresh.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)

            for con in contours:
                im = cv2.moments(con)

                if(im["m00"] != 0):
                    x = int(im["m10"] / im["m00"])
                    y = int(im["m01"] / im["m00"])
                else:
                    x = 0
                    y = 0

                cv2.drawContours(frame, [con], -1, (0, 255, 0), 2)
                cv2.circle(frame, (x, y), 7, (255, 255, 255), -1)

        # if drawBlobs: 
        #Blob detector will find points in the image.
        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(gray)

        #Draw the points on the color image.
        keyFrame = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        for k in range(len(keypoints)):
            point = keypoints[k]
            if drawBlobs:
                cv2.putText(keyFrame, str(k), (int(point.pt[0]) -10,int(point.pt[1]) +5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        if len(keypoints) > 1:
            #Brute Force Calculate nearest neighbors
            # If we were dealing with hundreds or more points, this would probably be inefficient,
            # But this is only ~20 points - so it was easier than setting up FLANN
            neighbors = {}
            for kp in range(len(keypoints)):
                neighbors[kp] = {}
                for nkp in range(len(keypoints)):
                    if kp == nkp:
                        continue
                    d = DistanceSquared(keypoints[kp].pt, keypoints[nkp].pt)
                    neighbors[kp][nkp] = d
                # Turn this into a dictionary of point ids to distance calculations.
                neighbors[kp] = dict(sorted(neighbors[kp].items(), key=lambda x: x[1]))
                
                # Ordered Neighbors list - nearest neighbors.
                # We don't actually care about the distance, because we don't use it to draw the line,
                # We just want to know _which_ id is the closest.
                on = list(neighbors[kp].keys())
                
                # Convert these values to integers to draw lines
                sx = int(keypoints[kp].pt[0])
                sy = int(keypoints[kp].pt[1])
                ex = int(keypoints[on[0]].pt[0])
                ey = int(keypoints[on[0]].pt[1])

                # I wanted to randomize colors, but it turned out to be too underground-rave/epilepsy-inducing.
                # r = getrandbits(8)
                # b = getrandbits(8)
                # g = getrandbits(8)
                # cv2.line(keyFrame, (sx,sy), (ex,ey), (r,b,g), 3)

                if drawLines:
                    cv2.line(keyFrame, (sx,sy), (ex,ey), (150, 150, 0), 3)

                # The distance in pixels of this point and its nearest neighbor
                pixelDistance = int(math.sqrt(list(neighbors[kp].values())[0]))

                #Calculate the distance to the camera using focal length constant and 
                distanceToCamera = (2 * focalLength)/pixelDistance
                if drawDistances:
                    cv2.putText(keyFrame, '{0}cm'.format(int(distanceToCamera)) ,(sx,sy-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 200), 1)

            if currentMode == Mode.DATA:
                cv2.imshow("disp", keyFrame)
        
        #Handle Different Display modes
        if currentMode == Mode.COLOR:
            cv2.imshow("disp",frame)
        elif currentMode == Mode.GRAY:
            cv2.imshow("disp",gray)
        elif currentMode == Mode.THRESH:
            cv2.imshow("disp",thresh)

        #Handle Key input        
        k = cv2.waitKey(1)
        if k == 49:
            currentMode = Mode.COLOR
        if k == 50:
            currentMode = Mode.GRAY
        if k == 51:
            currentMode = Mode.THRESH
        if k == 52:
            currentMode = Mode.DATA            
        if k == 98:
            drawBlobs = not drawBlobs
        if k == 100:
            drawDistances = not drawDistances
        if k == 108:
            drawLines = not drawLines
        if k == 27:
            break
        

def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("type")

    args = ap.parse_args()

    process_image(args.input, args.type)

if __name__ == '__main__':
    main()        


