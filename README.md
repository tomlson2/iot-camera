
# IP Camera Control
This project uses OpenCV and Onvif protocols to control an IP camera.

## Usage
To use the camera, first create an instance of the `IPCam` class. This will allow you to control the camera using the `absolute_move()` and `relative_move()` methods.

The `IPFeed` class allows you to access the image feed from the camera. This can be used to detect faces and center the camera on them.

## Example
The following code will use the `IPFeed` class to detect a face and move the camera to center it.
```python
from cam import IPCam, IPFeed

#example usage
def main():
    f = IPFeed()
    c = IPCam()

    while True:
        center = f.get_face_center()
        rel_pos = f.get_relative_pos(center)
        x_diff = 0.5 - rel_pos[0]
        y_diff = 0.5 - rel_pos[1]
        pan = 0
        tilt = 0
        if x_diff < -0.1:
            pan = 0.005
        elif x_diff > 0.1:
            pan = -0.
