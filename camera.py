from picamera import PiCamera
from time import sleep

# Creates the camera object
camera = PiCamera()
# 'Opens the shutter'
camera.start_preview()
# Leaves the shutter open
sleep(5)
# Saves the image
camera.capture('sample_image.jpg')
# Closes the shutter
camera.stop_preview()
