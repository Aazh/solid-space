import numpy as np
import cv2


def get_image():
    retval, im = camera.read()
    return im

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

camera = cv2.VideoCapture(0)


# Show image and close when esc is pressed
while True:
    i = 0
    while i != 30:
        temp = get_image()

        i = i + 1

    picture = get_image()
    picture2 = cv2.cvtColor(get_image(), cv2.COLOR_BGR2HSV)

    height = np.size(picture, 0)
    width = np.size(picture, 1)
    print(height)
    print(width)
    mask = np.zeros((height, width, 1), np.uint8)
    radius = 0
    target = 0

    cv2.namedWindow('pilt')
    cv2.createTrackbar('Brush size', 'pilt', 0, 500, setbrushsize)
    cv2.createTrackbar('target', 'pilt', 0, 2, settarget)
    cv2.setMouseCallback('pilt', draw_circle)

    while (1):
        cv2.imshow("pilt", picture)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            repeat = 0
            break
        elif k == ord('r'):
            repeat = 1
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
    #create/overwrite the targeted config file
    f = open('colorConfig' + str(target)+ '.txt', 'w')
    #write the HSV values to the new file
    txt = str(d)+'\n'+str(e)+'\n'+str(g)+'\n'+str(a)+'\n'+str(b)+'\n'+str(c)
    f.write(txt)
    #close the file
    f.close()
    #if repeat is set to 1, redo the whole process
    if repeat == 1:
        repeat = 0
    else:
        break
camera.release()
