import cv2
import numpy as np

print("before url")
cap = cv2.VideoCapture('rtsp://admin:iotcamera1@192.168.1.209:554/cam/realmonitor?channel=1&subtype=0')
print("after url")
while(True):
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()