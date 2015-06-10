#!/usr/bin/env python
import cv2
import numpy as np
rgb = np.uint8([[[255,255,0]]])
hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
print 'rgb',rgb,'hsv',hsv
