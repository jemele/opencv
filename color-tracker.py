#! /usr/bin/env python 

import cv2.cv as cv

color_tracker_window = "Color Tracker"

class ColorTracker:

    def __init__(self):
        cv.NamedWindow( color_tracker_window, 1 )
        self.capture = cv.CaptureFromCAM(0)
        cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_WIDTH,320)
        cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_HEIGHT,240)
        cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FPS,5.0)

    def run(self):
        while True:
            im = cv.QueryFrame(self.capture)
            img = cv.CloneImage(im)

            #blur the source image to reduce color noise 
            cv.Smooth(img, img, cv.CV_BLUR, 12);

            #convert the image to hsv(Hue, Saturation, Value) so its  
            #easier to determine the color to track(hue) 
            hsv = cv.CreateImage(cv.GetSize(img), 8, 3)
            cv.CvtColor(img, hsv, cv.CV_BGR2HSV)

            #limit all pixels that don't match our criteria, in this case we are  
            #looking for purple but if you want you can adjust the first value in  
            #both turples which is the hue range(120,140).  OpenCV uses 0-180 as  
            #a hue range for the HSV color model 
            threshold =  cv.CreateImage(cv.GetSize(hsv), 8, 1)
            ORANGE_MIN = cv.Scalar(20, 100, 100)
            ORANGE_MAX = cv.Scalar(30, 255, 255)
            cv.InRangeS(hsv, ORANGE_MIN, ORANGE_MAX, threshold)

            #determine the objects moments and check that the area is large  
            #enough to be our object 
            #thresholded_img = cv.GetMat(thresholded_img)
            moments = cv.Moments(cv.GetMat(threshold), 0)
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
                cv.Add(img, overlay, img)
                #add the thresholded image back to the img so we can see what was  
                #left after it was applied 
                #cv.Merge(thresholded_img, None, None, None, img)

            #display the image  
            cv.ShowImage(color_tracker_window, img)

            if cv.WaitKey(100) == 27:
                break

if __name__=="__main__":
    color_tracker = ColorTracker()
    color_tracker.run()
