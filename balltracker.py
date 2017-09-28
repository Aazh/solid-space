import cv2
import numpy as np
cap = cv2.VideoCapture(0)
# Load HSV values
g = open("config.txt")
huemax = int(g.readline())
satmax = int(g.readline())
intmax = int(g.readline())
huemin = int(g.readline())
satmin = int(g.readline())
intmin = int(g.readline())
def nothing(x):
    pass
g.close()
# Make trackbars for changing color ranges
cv2.namedWindow('frame')
cv2.createTrackbar('huemin','frame',huemin,179,nothing)
cv2.createTrackbar('satmin','frame',satmin,255,nothing)
cv2.createTrackbar('intmin','frame',intmin,255,nothing)
cv2.createTrackbar('huemax','frame',huemax,179,nothing)
cv2.createTrackbar('satmax','frame',satmax,255,nothing)
cv2.createTrackbar('intmax','frame',intmax,255,nothing)
while(1):
    # Set color ranges based on trackbars
    huemin = cv2.getTrackbarPos('huemin', 'frame')
    satmin = cv2.getTrackbarPos('satmin', 'frame')
    intmin = cv2.getTrackbarPos('intmin', 'frame')
    huemax = cv2.getTrackbarPos('huemax', 'frame')
    satmax = cv2.getTrackbarPos('satmax', 'frame')
    intmax = cv2.getTrackbarPos('intmax', 'frame')
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of orange color in HSV
    lower_orange = np.array([huemin,satmin,intmin])
    upper_orange = np.array([huemax,satmax,intmax])
    # Threshold the HSV image to get only orange colors
    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        # draw in blue the contours that were founded
        cv2.drawContours(res, contours, -1, 255, 3)

        # find the biggest area
        c = max(contours, key=cv2.contourArea)

        M = cv2.moments(c)
        try:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.circle(res, (cx, cy), 5, (0, 255, 0), -1)
        except:
            M = 0
        x, y, w, h = cv2.boundingRect(c)
        # draw the book contour (in green)
        cv2.rectangle(res, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("mask",mask)
    cv2.imshow('frame',frame)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
cap.release()
# Save HSV values
f = open("config.txt","w")
f.write(str(huemax)+"\n"+str(satmax)+"\n"+str(intmax)+"\n"+str(huemin)+"\n"+str(satmin)+"\n"+str(intmin)+"\n")
f.close()