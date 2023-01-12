import cv2
from cv_tools import load_faceCascade
from sensecam_control import onvif_control

'''
CAMERA INFO
IP (default assignment on IoT lab router) -> access camera settings at domain.
FEED_URL -> very specific format to grab rtsp feed, should not change.
'''
IP = '192.168.1.4'
LOGIN = 'admin'
PASSWORD = 'iotcamera1'
FEED_URL = f'rtsp://{LOGIN}:{PASSWORD}@{IP}:554/cam/realmonitor?channel=1&subtype=0'

class IPFeed:
    '''
    Collect image data from camera using OpenCV library.
    '''

    def __init__(self, url=FEED_URL) -> None:
        self.FEED = cv2.VideoCapture(url)
        self.faceCascade = load_faceCascade()
        self.h, self.w = self.get_im().shape[:2]

    def view_feed(self):
        while True:
            pass
    
    def get_im(self):
        _, im = self.FEED.read()
        return im
    
    def get_gray_im(self):
        gray_im = cv2.cvtColor(self.get_im(), cv2.COLOR_BGR2GRAY)
        return gray_im
    
    def find_faces(self):
        im = self.get_gray_im()
        faces = self.faceCascade.detectMultiScale(im, scaleFactor=1.2, minNeighbors=5,minSize=(20, 20))
        return faces
    
    def get_face_center(self, idx=0):
        x,y,w,h = self.find_faces()[idx]
        center = (x+(w/2),y+(h/2))
        return center
    
    def get_relative_pos(self, point):
        return point[0] / self.w, point[1] / self.h
        
    def face_centered_x(self):
        center = self.get_face_center()
        if 0.55 > (center[0] / self.w) > 0.45:
            return True
        return False
    
    def face_centered_y(self):
        center = self.get_face_center()
        if 0.55 > (center[1] / self.h) > 0.45:
            return True
        return False

class IPCam:

    '''
    IP Camera onvif protocols to control IPZ (camera) movement.
    
    Control Domains:
    PAN/TILT: -1.0 TO 1.0, ZOOM: 0.25 TO 1.0
    '''
    def __init__(self, ip=IP, login=LOGIN, password=PASSWORD) -> None:
        self.CAM = onvif_control.CameraControl(ip, login, password)
        self.CAM.camera_start()
        self.pan, self.tilt, self.zoom = self.get_PTZ_pos()

    def move_home(self):
        self.CAM.absolute_move(0, 0, 0)
    
    def update_pos(self, pan: float, tilt: float, zoom: float, relative:bool = False):
        if relative:
            self.pan += pan
            self.tilt += tilt
            self.zoom += zoom
        else:
            self.pan, self.tilt, self.zoom = pan, tilt, zoom

    def bounds_decorator(func):
        def wrapper(*args, **kwargs):
            self, pan, tilt, zoom = args
            if not -1.0 < self.pan + pan < 1.0:
                raise Exception("Pan input out of bounds")
            if not -1.0 < self.tilt + tilt < 1.0:
                raise Exception("Tilt input out of bounds")
            if not 0.25 < self.zoom + zoom < 1.0:
                raise Exception("Zoom input out of bounds")
            return func(*args, **kwargs)
        return wrapper

    def get_PTZ_pos(self): # pos values are not updated instantly after movement
        pan, tilt, zoom = self.CAM.get_ptz()
        return pan, tilt, zoom

    def absolute_move(self, pan: float, tilt: float, zoom: float):
        self.CAM.absolute_move(pan, tilt, zoom)
        self.update_pos(pan, tilt, zoom)
    
    # not working as intended, might have x/y signedness misconfigured
    #@bounds_decorator
    def relative_move(self, pan: float, tilt: float, zoom: float):
        self.CAM.relative_move(pan, tilt, zoom)
        self.update_pos(pan, tilt, zoom, relative=True)
