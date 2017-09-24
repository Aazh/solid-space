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
picture2 = cv2.cvtColor(get_image(), cv2.COLOR_BGR2HSV)

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
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
res = []
print(mask[0,0])
for x in range(0,width):
    for y in range(0,height):
        if mask[y,x] != [0]:
            res.append(picture2[y,x])
print(res[0][0])
print(len(res))
a,b,c,d,e,f = 0,0,0,999,999,999
for i in range(len(res)):
    a = max(a, res[i][0])
    b = max(b, res[i][1])
    c = max(c, res[i][2])
    d = min(d, res[i][0])
    e = min(e, res[i][1])
    g = min(f, res[i][2])
f = open("config.txt","w")
f.write(str(a)+"\n"+str(b)+"\n"+str(c)+"\n"+str(d)+"\n"+str(e)+"\n"+str(g)+"\n")
f.close()
print(a,b,c)
print(d,e,g)
