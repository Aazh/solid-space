import cv2
import numpy as np
cap = cv2.VideoCapture(0)
# Load HSV values
# Class for storing and getting HSV values
class Color:
    def __init__(self, colorConfig):
        f = open(colorConfig)
        self.index = colorConfig
        self.minhue = int(f.readline())
        self.minsat = int(f.readline())
        self.minint = int(f.readline())
        self.maxhue = int(f.readline())
        self.maxsat = int(f.readline())
        self.maxint = int(f.readline())
        f.close()

object_count = 3
# Stores the Color objects
objects = []
# Load values into objects
for i in range(object_count):
    color = Color('colorConfig' + str(i)+ ".txt")
    objects.append(color)
# function for
def get_color(index):
    color = objects[index]
    return color
# function for detecting coloured objects
def detect(index,hsv):
    cx = -1
    cy = -1
    # Threshold the HSV image to get only necessary colors
    color = get_color(index)
    lowerColor = np.array([color.minhue, color.minsat, color.minint])
    upperColor = np.array([color.maxhue, color.maxsat, color.maxint])
    mask = cv2.inRange(hsv, lowerColor, upperColor)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:

        # find the biggest area
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        area = cv2.minAreaRect(c)
        try:
            known_dist = 0.15
            known_width = 0.04
            focal_length = 649
            distance = known_width * focal_length / area[1][0]
         #   print(distance)

            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.circle(res, (cx, cy), 5, (0, 255, 0), -1)
        except:
            M = 0
            cx = -1
            cy = -1
        x, y, w, h = cv2.boundingRect(c)
        # draw the book contour (in green)
        cv2.rectangle(res, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return res, mask, cx, cy

def nothing(x):
    pass
#function for switching tracbars for different objects
def setrange(x):
    color = get_color(x)
    cv2.setTrackbarPos('huemin', 'frame', color.minhue)
    cv2.setTrackbarPos('satmin', 'frame', color.minsat)
    cv2.setTrackbarPos('intmin', 'frame', color.minint)
    cv2.setTrackbarPos('huemax', 'frame', color.maxhue)
    cv2.setTrackbarPos('satmax', 'frame', color.maxsat)
    cv2.setTrackbarPos('intmax', 'frame', color.maxint)


# Make trackbars for changing color ranges
cv2.namedWindow('frame')
cv2.createTrackbar('huemin','frame',0,179,nothing)
cv2.createTrackbar('satmin','frame',0,255,nothing)
cv2.createTrackbar('intmin','frame',0,255,nothing)
cv2.createTrackbar('huemax','frame',0,179,nothing)
cv2.createTrackbar('satmax','frame',0,255,nothing)
cv2.createTrackbar('intmax','frame',0,255,nothing)
cv2.createTrackbar('detect','frame',0,2,setrange)
setrange(0)
while(1):
    # Set color ranges based on trackbars
    color = get_color(cv2.getTrackbarPos('detect', 'frame'))
    color.minhue = cv2.getTrackbarPos('huemin', 'frame')
    color.minsat = cv2.getTrackbarPos('satmin', 'frame')
    color.minint = cv2.getTrackbarPos('intmin', 'frame')
    color.maxhue = cv2.getTrackbarPos('huemax', 'frame')
    color.maxsat = cv2.getTrackbarPos('satmax', 'frame')
    color.maxint = cv2.getTrackbarPos('intmax', 'frame')
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Detect objects and their positions
    res1, mask1, cx1, cy1 = detect(0, hsv)
    res2, mask2, cx2, cy2 = detect(1, hsv)
    res3, mask3, cx3, cy3 = detect(2, hsv)
    # Make a bunch of windows
    cv2.imshow('frame',frame)
    cv2.imshow('res1',res1)
    cv2.imshow('res2', res2)
    cv2.imshow('res3', res3)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
cap.release()
# Save HSV values
for i in range(object_count):
    f = open('colorConfig' + str(i)+ ".txt","w")
    # Save values to a string
    color = get_color(i)
    txt = (str(color.minhue)+"\n"+str(color.minsat)+"\n"+str(color.minint)+"\n"+str(color.maxhue)+"\n"+str(color.maxsat)+"\n"+str(color.maxint)+"\n")
    # Write the string to file
    f.write(txt)
    f.close()