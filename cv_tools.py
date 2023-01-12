import os
import cv2

def load_faceCascade():
    CASCPATH=os.path.dirname(cv2.__file__)+"/data/haarcascade_frontalface_default.xml"
    return cv2.CascadeClassifier(CASCPATH)