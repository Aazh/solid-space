import numpy as np
import cv2

camera = cv2.VideoCapture(1)

def get_image():
    retval, im = camera.read()
    return im
i = 0
while i != 30:
    temp = get_image()
    i = i + 1
file = "C:\Pildid\pall.png"

camera_capture = get_image()

cv2.imwrite(file, camera_capture)

del(camera)