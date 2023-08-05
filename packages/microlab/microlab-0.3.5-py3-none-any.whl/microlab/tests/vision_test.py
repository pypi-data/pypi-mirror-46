from microlab.Vision import Camera
import time

cam = Camera(index=0)
cam.connect()
cam.start()
time.sleep(1)
cam.stop()
cam.disconnect()

print('Camera: {} '.format(type(cam)))
