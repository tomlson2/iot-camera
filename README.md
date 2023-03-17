
# SenseCam

## Overview

SenseCam is a Python library for controlling IP cameras. It provides a set of tools for accessing camera feeds and controlling the camera's pan, tilt and zoom.

## Usage

The main entry point for SenseCam is the `IPCam` class. This class provides methods for controlling the camera's pan, tilt and zoom.

```python
from cam import IPCam, IPFeed

# Create an instance of the IPCam class
c = IPCam()

# Move the camera to the home position
c.move_home()

# Move the camera relative to its current position
c.relative_move(pan, tilt, zoom)

# Get the camera's current position
pan, tilt, zoom = c.get_PTZ_pos()
```

The `IPFeed` class provides methods for accessing the camera's feed.

```python
# Create an instance of the IPFeed class
f = IPFeed()

# Get the camera's current image
im = f.get_im()

# Get the camera's current grayscale image
gray_
