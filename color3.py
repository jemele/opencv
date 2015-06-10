import cv2
import cv2.cv as cv
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,240)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,320)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    lower = cv2.cvtColor(np.uint8([[[255,255,0]]]),cv2.COLOR_RGB2HSV)
    hue = lower[0][0][0]
    lower = np.uint8([[[ hue - 10, 100, 100 ]]])
    upper = np.uint8([[[ hue, 255, 255 ]]])
    print 'lower',lower
    print 'upper',upper

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower, upper)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()

