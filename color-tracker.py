#! /usr/bin/env python 
import cv2
import cv2.cv as cv
import numpy as np

def nothing(x):
    pass

class ColorTracker:

    def __init__(self):
        self.capture = cv.CaptureFromCAM(0)
        cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_WIDTH,320)
        cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_HEIGHT,240)
        cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FPS,5.0)

        # Starting with 100's to prevent error while masking
        h0,s0,v0 =0,130,13
        h1,s1,v1= 29,175,62

        # Creating track bar
        cv2.namedWindow('controls')
        cv2.createTrackbar('h0','controls',h0,179,nothing)
        cv2.createTrackbar('s0','controls',s0,255,nothing)
        cv2.createTrackbar('v0','controls',v0,255,nothing)
        cv2.createTrackbar('h1','controls',h1,179,nothing)
        cv2.createTrackbar('s1','controls',s1,255,nothing)
        cv2.createTrackbar('v1','controls',v1,255,nothing)

    def run(self):
        while True:
            im = cv.QueryFrame(self.capture)
            img = cv.CloneImage(im)

            #blur the source image to reduce color noise 
            cv.Smooth(img, img, cv.CV_BLUR, 2);

            #convert the image to hsv(Hue, Saturation, Value) so its  
            #easier to determine the color to track(hue) 
            hsv = cv.CreateImage(cv.GetSize(img), 8, 3)
            cv.CvtColor(img, hsv, cv.CV_BGR2HSV)

            #limit all pixels that don't match our criteria, in this case we are  
            #looking for purple but if you want you can adjust the first value in  
            #both turples which is the hue range(120,140).  OpenCV uses 0-180 as  
            #a hue range for the HSV color model 
            threshold = cv.CreateImage(cv.GetSize(hsv), 8, 1)

            # get info from track bar and appy to result
            h0 = cv2.getTrackbarPos('h0','controls')
            s0 = cv2.getTrackbarPos('s0','controls')
            v0 = cv2.getTrackbarPos('v0','controls')

            h1 = cv2.getTrackbarPos('h1','controls')
            s1 = cv2.getTrackbarPos('s1','controls')
            v1 = cv2.getTrackbarPos('v1','controls')

            # these need to be tuned to a color.
            # it would be awesome to sample and learn.
            COLOR_MIN = cv.Scalar(h0, s0, v0)
            COLOR_MAX = cv.Scalar(h1, s1, v1)
            cv.InRangeS(hsv, COLOR_MIN, COLOR_MAX, threshold)

            #determine the objects moments and check that the area is large  
            #enough to be our object 
            #thresholded_img = cv.GetMat(thresholded_img)
            threshold = cv.GetMat(threshold)
            moments = cv.Moments(threshold, 0)
            area = cv.GetCentralMoment(moments, 0, 0)

            #there can be noise in the video so ignore objects with small areas 
            if area > 100000:
                #determine the x and y coordinates of the center of the object 
                #we are tracking by dividing the 1, 0 and 0, 1 moments by the area 
                x = cv.GetSpatialMoment(moments, 1, 0)/area
                y = cv.GetSpatialMoment(moments, 0, 1)/area
                print 'x',x,'y',y,'area',area
                
                #create an overlay to mark the center of the tracked object 
                overlay = cv.CreateImage(cv.GetSize(img), 8, 3)
                cv.Circle(overlay, (int(x), int(y)), 2, (255, 255, 255), 20)
                cv.ShowImage('threshold', threshold)
                cv.ShowImage('overlay', overlay)

            #display the image  
            cv.ShowImage('capture', img)

            if cv.WaitKey(10) == 27:
                break

if __name__=="__main__":
    color_tracker = ColorTracker()
    color_tracker.run()
