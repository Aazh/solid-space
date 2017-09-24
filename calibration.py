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
picture2 = get_image()

height = np.size(picture,0)
width = np.size(picture,1)
print(height)
print(width)
mask = np.zeros((height, width, 1), np.uint8)
radius = 0
def setbrushsize(int):
    global radius
    radius = int

def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(mask, (x, y), radius, (255, 255, 255), -1)
        cv2.circle(picture, (x, y), radius, (255, 255, 255), -1)


cv2.namedWindow('pilt')
cv2.createTrackbar('Brush size','pilt',0,500,setbrushsize)
cv2.setMouseCallback('pilt', draw_circle)

camera.release()
while(1):
    cv2.imshow("pilt",picture)
    cv2.imshow("mask", mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
res = []
print(mask[0,0])
for x in range(0,width):
    for y in range(0,height):
        if mask[y,x] != [0]:
            res.append(picture2[y,x])
print(res)

cv2.destroyAllWindows()