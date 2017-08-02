import numpy as np
import cv2



cap = cv2.VideoCapture(0) #built in camera


cv2.namedWindow('image', 0)#create trackbar window
#check = np.zeros((300,512,3), np.uint8)

#Pass function
def nothing(x):
    pass

#TrackBars for HSV
#Lower HSV
cv2.createTrackbar('LH','image',0,255,nothing)
#cv2.createTrackbar('LS','image',0,255,nothing)
#cv2.createTrackbar('LV','image',0,255,nothing)

#Upper HSV
cv2.createTrackbar('UH','image',0,255,nothing)
#cv2.createTrackbar('US','image',0,255,nothing)
#cv2.createTrackbar('UV','image',0,255,nothing)

#Switch
cv2.createTrackbar('Change Colour', 'image', 0, 1, nothing)


#actual code
while (1):
    #cap = cv2.VideoCapture('http://192.168.20.115:8080/shot.jpg?rnd=607675') #URL Streaming
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #checkHsv = cv2.cvtColor(check, cv2.COLOR_BGR2HSV)
    lH = cv2.getTrackbarPos('LH','image')

    uH = cv2.getTrackbarPos('UH','image')


    if (cv2.getTrackbarPos('Change Colour', 'image') == 0):
        lowerYellow = np.array([90, 100, 100])
        higherYellow = np.array([100, 255, 255])
    else:
        lowerYellow = np.array([lH, 100, 100])
        higherYellow = np.array([uH, 255, 255])

    frame = cv2.flip(frame, 1)
    mask = cv2.inRange(hsv, lowerYellow, higherYellow)
    mask =cv2.flip(mask, 1)
    #res = cv2.bitwise_and(frame,frame, mask= mask)
    #checkHsv[:] = [lH,lS,lV]

    _, contours,  _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0: #checks if any contours are found
        circle = max(contours, key = cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(circle)
        M = cv2.moments(circle)
        if (M["m00"] != 0):
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            cv2.line(frame, (320,240), center, (0,0,255), 5)

            #print(center)
    cv2.imshow('frame' ,frame)
    cv2.imshow('mask' ,mask)
    #cv2.imshow('result' ,res)
    #cv2.imshow('image', checkHsv)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()