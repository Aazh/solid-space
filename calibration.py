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
cv2.createTrackbar('target','pilt',0,2,settarget)
cv2.setMouseCallback('pilt', draw_circle)

camera.release()
# Show image and close when esc is pressed
while(1):
    cv2.imshow("pilt",picture)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
res = []
# Make a list of selected HSV values
print(mask[0,0])
for x in range(0,width):
    for y in range(0,height):
        if mask[y,x] != [0]:
            res.append(picture2[y,x])
print(res[0][0])
print(len(res))
a,b,c,d,e,f = 0,0,0,999,999,999
#define minimum and maximum HSV values
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
if str(h.read()).count("\n") != 18:
    h.close()
    h = open("config.txt", "w")
    h.write("0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n")
    h.close()
else:
    h.close()
# Make a list for storing  HSV values
txt = []
h = open("config.txt")
# Append values from file to list
while True:
    s = h.readline().strip()
    if s != "":
        txt.append(s)
    else:
        break
# Define the target range
t = target * 6
# Change targeted values to the new values
txt[t] = a
txt[t+1] = b
txt[t+2] = c
txt[t+3] = d
txt[t+4] = e
txt[t+5] = g
config = ""
f = open("config.txt", "w")
for i in range(0,len(txt)):
    config = config + str(txt[i]) + "\n"
f.write(config)
f.close()
print(a,b,c)
print(d,e,g)
