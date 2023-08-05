from microlab.Cameras import Camera
import time

# Initialize camera object
cam = Camera(index=0)

# connect to camera
cam.connect()

# start the recording
cam.start()

# let the camera stream open for a while
time.sleep(1)

# stop the recording
cam.stop()

# disconnect from camera
cam.disconnect()

# save the images
cam.export(path='images')

print('Camera: {} '.format(type(cam)))
