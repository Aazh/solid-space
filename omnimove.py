import cv2
from movement_functions import liigu
import numpy as np
import serial

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = int(round(rho * np.cos(phi), 0))
    y = int(round(rho * np.sin(phi), 0))
    return(x, y)

def draw_circle(event, fx, fy, flags, param):
    global rho
    global phi
    if event == cv2.EVENT_LBUTTONDBLCLK:
        x = (fx - 250)
        y = -(fy - 250)
        rho, phi = cart2pol(x, y)
def setSpeed():
    pass
speed = 0
port = 'COM3'
ser = serial.Serial(
    port=port,
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS
)
cv2.namedWindow("kontroll")
cv2.createTrackbar('speed','kontroll',0,50,setSpeed)
height = 500
width = 500
x = 0
y = 0
rho, phi = cart2pol(x, y)
rho = 0
cv2.setMouseCallback('kontroll', draw_circle)
i = 0
while True:
    x, y = pol2cart(rho, phi)
    #print(x, y, rho, phi)
    k = cv2.waitKey(5) & 0xFF
    image = np.zeros((height, width, 3), np.uint8)
    cv2.circle(image, (250, 250), 250, (255, 255, 255), -1)
    cv2.circle(image, (250, 250), 3, (255, 0, 0), -1)
    if x != 0 and y != 0:
        cv2.circle(image, (x + 250, (-y) + 250), 5, (0, 0, 250), -1)
    if rho > 0:
        rho -= 1
    if rho < 0:
        rho = 0
    #print(x, y, rho, phi)

    speed = (cv2.getTrackbarPos('speed', 'kontroll'))/100

    i += 1
    if i % 10 == 0:
        if rho != 0 and k != ord("q") and k != ord("e"):
            liigu(speed, phi, 0, ser)

        elif k == ord("q"):
            liigu(speed, phi, 0.5, ser)

        elif k == ord("e"):
            liigu(speed, phi, -0.5, ser)

        else:
            liigu(0, 0, 0, ser)





    cv2.imshow('kontroll', image)

    if k == 27:
        break
ser.close()
cv2.destroyAllWindows()