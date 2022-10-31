import cv2
import os


cascPath=os.path.dirname(cv2.__file__)+"/data/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

print("before url")
cap = cv2.VideoCapture('rtsp://admin:iotcamera1@192.168.1.209:554/cam/realmonitor?channel=1&subtype=0')
print("after url")

while(True):
    ret, img = cap.read()
    img = cv2.flip(img, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale(
        gray,     
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(20, 20)
    )
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]  
    cv2.imshow('video',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    ret = cap.grab()


cap.release()
cv2.destroyAllWindows()