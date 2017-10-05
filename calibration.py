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
target = 0

def setbrushsize(int):
    global radius
    radius = int

def settarget(int):
    global target
    target = int

def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(mask, (x, y), radius, (255, 255, 255), -1)
        cv2.circle(picture, (x, y), radius, (255, 255, 255), -1)


cv2.namedWindow('pilt')
cv2.createTrackbar('Brush size','pilt',0,500,setbrushsize)
cv2.createTrackbar('target','pilt',0,1,settarget)
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
#if it fails to open the config file, create a new one
try:
    h = open("config.txt")
except:
    h = open("config.txt", "w")
    h.close()
    h = open("config.txt")
#if the config file is filled incorrectly, fill it with 12 zeroes
if str(h.read()).count("\n") != 12:
    h.close()
    h = open("config.txt", "w")
    h.write("0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n")
    h.close()
else:
    h.close()
h = open("config.txt")
#if the target is zero, overwrite values 1-6 and preserve everything after that
if target == 0:
    for i in range(6):
        h.readline()
    txt = h.read()
    h.close()
    f = open("config.txt", "w")
    f.write(str(a) + "\n" + str(b) + "\n" + str(c) + "\n" + str(d) + "\n" + str(e) + "\n" + str(g) + "\n" + txt)
    f.close()
#if the target is one, preserve values 1-6 and overwrite values 7-12
else:
    txt = ""
    for i in range(6):
        txt = txt + h.readline()
    h.close()
    f = open("config.txt", "w")
    f.write(txt + str(a)+"\n"+str(b)+"\n"+str(c)+"\n"+str(d)+"\n"+str(e)+"\n"+str(g)+"\n")
    f.close()

print(a,b,c)
print(d,e,g)
