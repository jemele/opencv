# https://li8bot.wordpress.com/2014/07/13/opencvpythonpart-3-tracking-object-using-colorspaces/
import cv2.cv as cv

def getThresholdImage(im):
    newim = cv.CloneImage(im)
    cv.Smooth(newim, newim, cv.CV_BLUR,12) #Remove noise

    hsv=cv.CreateImage(cv.GetSize(im), 8, 3)
    cv.CvtColor(newim, hsv, cv.CV_BGR2HSV) # Convert image to HSV
    threshold = cv.CreateImage(cv.GetSize(im), 8, 1)
    #Do the threshold on the hsv image, with the right range for the yellow color
    cv.InRangeS(hsv, cv.Scalar(20, 100, 100), cv.Scalar(30, 255, 255), threshold)
    del hsv
    return threshold


capture = cv.CaptureFromCAM(0)
cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,240)
cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,320)

cv.NamedWindow("video")
cv.NamedWindow("thresh")

tmp = cv.QueryFrame(capture)

posx = 0
posy = 0

while True:
    frame = cv.QueryFrame(capture)
    thresh = getThresholdImage(frame) #Apply the threshold function
    moments = cv.Moments(cv.GetMat(thresh),1)
    moment10 = cv.GetSpatialMoment(moments, 1, 0)
    moment01 = cv.GetSpatialMoment(moments, 0, 1)
    area = cv.GetCentralMoment(moments, 0, 0) #Get the center

    lastx = posx
    lasty = posy
    if area == 0:
        posx = 0
        posy = 0
    else:
        posx = moment10/area
        posy = moment01/area

    if lastx > 0 and lasty > 0 and posx > 0 and posy > 0: #Mean we have received coordinates to print
        overlay = cv.CreateImage(cv.GetSize(tmp), 8, 3) #Image that will contain lines
        cv.Circle(overlay, (int(posx),int(posy)), 2, cv.Scalar(255,255,255),20)
        cv.Add(frame, overlay, frame)
        cv.ShowImage("overlay", overlay)

    cv.ShowImage("video", frame)
    cv.ShowImage("thresh", thresh)
    c=cv.WaitKey(1)
    if c==27 or c==1048603: #Break if user enters 'Esc'.
        break
    elif c== 1048690: # 'r' for reset
        cv.Zero(imgScribble)
