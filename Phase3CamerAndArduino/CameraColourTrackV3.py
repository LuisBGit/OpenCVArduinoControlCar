#Camera Tracking Version 2
#Tracks the colour of your choice
#Author: Luis Borja

#Import Requried Libraries
import numpy as np
import cv2
import _thread
from tkinter import *
import math
import serial

ser = serial.Serial('COM4', 38400, timeout=0)

#Pass functions dont know why it doesnt work normally
def nothing(x):
    pass

#mouse control for movement
def drawTarget(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        param.markTarget(x,y)
    if event == cv2.EVENT_RBUTTONDBLCLK:
        param.removePoint()

#Filter and Window class, controls the frames and video feed
class myFilter:
    def __init__(self, inputFrame, colourSwap, trackbars, name):
        self.frame = inputFrame
        self.targetX = 0
        self.targetY = 0
        self.target = False
        self.firstTracker = 0
        self.secondTracker = 0
        self.storedColour = colourSwap
        self.changeColour(trackbars)
        cv2.namedWindow(name)

    def changeColour(self,trackbarIn):
        if (self.storedColour == "HSV"):
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            self.frame = cv2.inRange(self.frame, trackbarIn.getLowerPos(), trackbarIn.getUpperPos())
        elif (self.storedColour == "GRAY"):
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)


    def displayFrame(self, title):
        cv2.imshow(title, self.frame)

    def updateFrame(self, inputFrame, trackbarIn):
        self.frame = inputFrame
        self.frame = cv2.flip(self.frame, 1)
        self.changeColour(trackbarIn)

    def detectContour(self):
        _,contours,_ = cv2.findContours(self.frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def trackObject(self, contours, trackNumber):
        if len(contours) > 0:  # checks if any contours are found
            circle = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(circle)
            M = cv2.moments(circle)
            if (M["m00"] != 0):
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                if (trackNumber == 1):
                    self.firstTracker = center
                else:
                    self.secondTracker = center
                cv2.circle(self.frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(self.frame, center, 5, (0, 0, 255), -1)

                if self.target == True:
                    cv2.line(self.frame, (self.targetX, self.targetY), center, (0, 0, 255), 5)

    def markTarget(self,x, y):
        print("DRAW")
        print("Drawing")
        self.targetX = x
        self.targetY = y
        self.target = True

    def drawPoint(self):
        if self.target == True:
            cv2.circle(self.frame, (self.targetX,self.targetY), 7, (0, 0, 255), 4)
    def removePoint(self):
        if self.target == True:
            self.target = False

    def lineCheck(self):

        x1 = self.firstTracker[0]
        y1 = self.firstTracker[1]
        x2 = self.secondTracker[0]
        y2 = self.secondTracker[1]

        if (self.target == True):
            linex1 = self.targetX - x1
            liney1 = self.targetY - y1
            line1Length = math.hypot(linex1, liney1)
            angleOut1 = (math.atan2(liney1,linex1) * 180 / math.pi)

            linex2 = self.targetX - x2
            liney2 = self.targetY - y2
            line2Length = math.hypot(linex2, liney2)
            angleOut2 = (math.atan2(liney2,linex2) * 180/ math.pi)

            if (line2Length < 100):
                self.target = False
            else:
                self.runMotor(angleOut1,angleOut2, line1Length, line2Length)
            #if self.closeEnough(angleOut1, angleOut2):
                #print("IN LINE")



    def runMotor(self, ref, angle2, LengthRef, Length2):
        global ser
        stringOut = "0,0,"
        gain = 0.15
        constant = 150

        if (self.closeEnough(ref, angle2, LengthRef, Length2) == False):
            leftMotor = 140
            rightMotor = -140
        else: #150, 150
            error = ref - angle2
            leftMotor = constant - (gain * error)
            rightMotor = constant + (gain * error)
            leftMotor = self.withinRange(leftMotor, -180, 180)
            rightMotor = self.withinRange(rightMotor, -180, 180)

        stringOut = str(leftMotor) + "," + str(rightMotor) + ","
        print(stringOut)
        ser.write(bytes(stringOut, "ascii"))


    def closeEnough(self, angle1, angle2, Length1, Length2):
        lowerLimit1 = angle1 - 10 #20 for defualt
        upperLimit1 = angle1 + 10

        if ((angle2 > lowerLimit1) & (angle2 < upperLimit1)):
            if(Length1 > Length2):
                return True
            else:
                return False
        else:
            return False

    def withinRange(self, value, lowerLimit, upperLimit):
        if (value < lowerLimit):
            value = lowerLimit
        elif (value > upperLimit):
            value = upperLimit

        return value

#Main loop that calls the filter objects
def cameraLoop(trackbars, trackbar2):
    global ser
    cap = cv2.VideoCapture('http://172.23.83.65:8080/shot.jpg?rnd=297133')
    state, frame = cap.read()

    Test = myFilter(frame, "A", trackbars, "frame")
    lightBlue = myFilter(frame, "HSV", trackbars, "lightBlue")
    red = myFilter(frame, "HSV", trackbars, "red")

    cv2.setMouseCallback("frame", drawTarget, param= Test)
    while (1):
        cap = cv2.VideoCapture('http://172.23.83.65:8080/shot.jpg?rnd=297133')
        state, frame = cap.read()

        #Apply Filter
        hsv = frame
        Test.updateFrame(frame, trackbars)
        lightBlue.updateFrame(hsv, trackbars)
        red.updateFrame(hsv, trackbar2)

        #Apply Tracking
        Test.trackObject(lightBlue.detectContour(), 1)
        Test.trackObject(red.detectContour(), 2)

        #Target
        Test.drawPoint()
        Test.lineCheck()

        #Display
        Test.displayFrame("frame")
        lightBlue.displayFrame("lightBlue")
        red.displayFrame("red")


        k = cv2.waitKey(5) & 0xFF #DO NOT REMOVE
        if k == 27:
            break

#trackbar controls colours
class Trackbars():
    def __init__(self,master):
        tkFrame = Frame(master)
        tkFrame.pack()

        self.lowerSlider = Scale(tkFrame, from_=0, to_=255, orient=VERTICAL)
        self.lowerSlider.pack(side=LEFT)

        self.upperSlider = Scale(tkFrame, from_=0, to_=255, orient=VERTICAL)
        self.upperSlider.set(150)
        self.upperSlider.pack(side=LEFT)

    def getLowerPos(self):
        lowerRange = np.array([self.lowerSlider.get(),100,100])
        return lowerRange
    def getUpperPos(self):
        upperRange = np.array([self.upperSlider.get(),255,255])
        return upperRange


#main function
if __name__ == "__main__":

    root = Tk()
    tracks = Trackbars(root)
    trackTwo = Trackbars(root)
    _thread.start_new_thread(cameraLoop, (tracks,trackTwo))
    root.mainloop()


    #put in seperate function thread

    cv2.destroyAllWindows()

