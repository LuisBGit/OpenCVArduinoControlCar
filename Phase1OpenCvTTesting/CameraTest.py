import numpy as np
import cv2

cap = cv2.VideoCapture(0)

def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(frame, (x,y), 100, (255,0,0), - 1)

cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

        # Our operations on the frame come here
    frame = cv2.circle(frame, (320,240), 60, (0,255,0),20)
    frame = cv2.flip(frame, 1)
    height, width, channels = frame.shape
    # Display the resulting frame
    cv2.imshow('image',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()