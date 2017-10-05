import cv2
import numpy as np
cap = cv2.VideoCapture(0)
# Load HSV values
g = open("config.txt")
upperColor1 = np.array([int(g.readline()), int(g.readline()), int(g.readline())])
lowerColor1 = np.array([int(g.readline()), int(g.readline()), int(g.readline())])
upperColor2 = np.array([int(g.readline()), int(g.readline()), int(g.readline())])
lowerColor2 = np.array([int(g.readline()), int(g.readline()), int(g.readline())])
upperColor3 = np.array([int(g.readline()), int(g.readline()), int(g.readline())])
lowerColor3 = np.array([int(g.readline()), int(g.readline()), int(g.readline())])
# function for detecting coloured objects
def detect(lowerColor,upperColor,hsv):
    cx = -1
    cy = -1
    # Threshold the HSV image to get only necessary colors
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
    if x == 0:
        minrange = lowerColor1
        maxrange = upperColor1
    elif x == 1:
        minrange = lowerColor2
        maxrange = upperColor2
    elif x == 2:
        minrange = lowerColor3
        maxrange = upperColor3
    cv2.setTrackbarPos('huemin', 'frame', minrange[0])
    cv2.setTrackbarPos('satmin', 'frame', minrange[1])
    cv2.setTrackbarPos('intmin', 'frame', minrange[2])
    cv2.setTrackbarPos('huemax', 'frame', maxrange[0])
    cv2.setTrackbarPos('satmax', 'frame', maxrange[1])
    cv2.setTrackbarPos('intmax', 'frame', maxrange[2])

g.close()
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
    huemin = cv2.getTrackbarPos('huemin', 'frame')
    satmin = cv2.getTrackbarPos('satmin', 'frame')
    intmin = cv2.getTrackbarPos('intmin', 'frame')
    huemax = cv2.getTrackbarPos('huemax', 'frame')
    satmax = cv2.getTrackbarPos('satmax', 'frame')
    intmax = cv2.getTrackbarPos('intmax', 'frame')
    if cv2.getTrackbarPos('detect', 'frame') == 0:
        lowerColor1 = np.array([huemin, satmin, intmin])
        upperColor1 = np.array([huemax, satmax, intmax])
    elif cv2.getTrackbarPos('detect', 'frame') == 1:
        lowerColor2 = np.array([huemin, satmin, intmin])
        upperColor2 = np.array([huemax, satmax, intmax])
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Detect objects and their positions
    res1, mask1, cx1, cy1 = detect(lowerColor1, upperColor1, hsv)
    res2, mask2, cx2, cy2 = detect(lowerColor2, upperColor2, hsv)
    res3, mask3, cx3, cy3 = detect(lowerColor3, upperColor3, hsv)
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
f = open("config.txt","w")
# Save values to a string
txt = (str(upperColor1[0])+"\n"+str(upperColor1[1])+"\n"+str(upperColor1[2])+"\n"+str(lowerColor1[0])+"\n"+str(lowerColor1[1])+"\n"+str(lowerColor1[2])+"\n")
txt = (txt + str(upperColor2[0])+"\n"+str(upperColor2[1])+"\n"+str(upperColor2[2])+"\n"+str(lowerColor2[0])+"\n"+str(lowerColor2[1])+"\n"+str(lowerColor2[2])+"\n")
txt = (txt + str(upperColor3[0])+"\n"+str(upperColor3[1])+"\n"+str(upperColor3[2])+"\n"+str(lowerColor3[0])+"\n"+str(lowerColor3[1])+"\n"+str(lowerColor3[2]))
# Write the string to file
f.write(txt)
f.close()