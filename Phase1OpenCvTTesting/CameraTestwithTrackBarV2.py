import numpy as np
import cv2

ix,iy = -1, -1

cap = cv2.VideoCapture(0)

def nothing(x):
    pass


def mousePos(event, x, y, flags, param):
    global ix, iy
    if event == cv2.EVENT_LBUTTONDBLCLK:
        ix, iy = x,y

cv2.namedWindow('image')
cv2.createTrackbar('R','image',0,255,nothing)
cv2.createTrackbar('G','image',0,255,nothing)
cv2.createTrackbar('B','image',0,255,nothing)
cv2.setMouseCallback('image', mousePos)

while(True):
    print(ix,iy)
    # Capture frame-by-frame
    ret, frame = cap.read()

        # Our operations on the frame come here
    frame = cv2.circle(frame, (320,240), 60, (0,255,0),20)
    frame = cv2.flip(frame, 1)
    height, width, channels = frame.shape
    r = cv2.getTrackbarPos('R', 'image')
    g = cv2.getTrackbarPos('G', 'image')
    b = cv2.getTrackbarPos('B', 'image')
    frame[:] = [b,g,r]
    # Display the resulting frame
    cv2.imshow('image',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()