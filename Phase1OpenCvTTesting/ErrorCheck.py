
import cv2


# class myFilter:
#
#     def __init__(self,inputFrame, colourSwap):
#         self.frame = inputFrame
#         self.changeColour(colourSwap)
#         self.displayFrame()
#
#     def changeColour(self,colourInput):
#         if (colourInput == "HSV"):
#             self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
#         elif (colourInput == "GRAY"):
#             self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
#
#     def displayFrame(self):
#         cv2.imshow('frame', self.frame)
#
#     def updateFrame(self,inputFrame):
#         self.frame = inputFrame

cap = cv2.VideoCapture(0)
# Test = myFilter(frame, "A")
# Test.displayFrame()

while (1):
    _, frame = cap.read()
    cv2.imshow('frame', frame)
    print(__name__)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
