# http://www.technicdynamic.com/2017/08/28/python-motion-detection-with-opencv-simple/

import numpy as np		      # importing Numpy for use w/ OpenCV
import cv2                            # importing Python OpenCV
from datetime import datetime         # importing datetime for naming files w/ timestamp
import csv
import os
import sys


############################# Function to calculate difference between images....
def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return  cv2.bitwise_and(d1,d2)


######################### Threshold for triggering "motion detection"
#threshold = 110000

threshold = sys.argv[1]
threshold = int(float(threshold))

cam = cv2.VideoCapture(1)
#cam = cv2.VideoCapture("people-walking.mp4")

winName = "Movement Indicator"	      # comment to hide window
cv2.namedWindow(winName)              # comment to hide window

# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
# Lets use a time check so we only take 1 pic per sec
timeCheck = datetime.now().strftime('%Ss')

with open('/home/jcgonzalez/Documentos/Proyectos/cv_cosas/detectorMovFot/Salida.csv','w') as csvfile:
    fieldnames = ['Date/Time','Threshold','totalDiffe','file']
    writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
    writer.writeheader()


    while True:
        ret, frame = cam.read()
        totalDiff = cv2.countNonZero(diffImg(t_minus, t, t_plus))     # this is total difference number
        text = "threshold: " + str(totalDiff)                # make a text showing total diff.
        cv2.putText(frame, text, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)   # display it on screen
        if totalDiff > threshold and timeCheck != datetime.now().strftime('%Ss'):
            dimg= cam.read()[1]
            #cv2.imwrite(datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + '.jpg', dimg)
            #-------------------------------------------------------------------------------------
            nameFile   = datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + '.jpg'
            nameFolder = './data/'
            pathName = nameFolder+nameFile
            datatiempo = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            cv2.imwrite(pathName, cv2.resize(dimg,(800,600)))
            #print (datatiempo, threshold, totalDiff, nameFile)
            writer.writerow({'Date/Time': datatiempo,'Threshold' : threshold, 'totalDiffe' : totalDiff, 'file' : nameFile})
            #-------------------------------------------------------------------------------------
        timeCheck = datetime.now().strftime('%Ss')
        # Read next image
        t_minus = t
        t = t_plus
        t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
        cv2.imshow(winName, frame)

        key = cv2.waitKey(10)
        if key == 27:      # comment this 'if' to hide window
            cv2.destroyWindow(winName)
            break

cam.release()
