#!/usr/bin/env python
import cv2
c = cv2.VideoCapture(0)
c.set(cv2.cv.CV_CAP_PROP_FPS,5)
c.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,240)
c.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,320)
