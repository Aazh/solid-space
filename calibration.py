import numpy as np
import cv2

camera = cv2.VideoCapture(0)

def get_image():
    retval, im = camera.read()
    return im
i = 0
while i != 30:
    temp = get_image()
    i = i + 1

picture = get_image()

camera.release()
while(1):
    imshow(picture)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()