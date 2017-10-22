from detection_functions import detector
from movement_functions import liigu
from math import pi
from time import time
import cv2
import serial

cap = cv2.VideoCapture(1)
port = 'COM3'

ser = serial.Serial(
    port=port,
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS
)
t = time() + 2
state = 'search and destroy'
try:
    detectors = []
    for i in range(3):
        looker = detector('colorConfig{0}.txt'.format(i), i)
        detectors.append(looker)


    cv2.namedWindow("kontroll")


    while True:

        if state == 'search and destroy':

            if t < time():
                t = time() + 2
                ser.close()
                ser = serial.Serial(
                    port=port,
                    baudrate=115200,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_TWO,
                    bytesize=serial.EIGHTBITS
                )

            ret, mask, x, y = detectors[0].detect(cap)
            cv2.imshow('kontroll', ret)
            k = cv2.waitKey(5) & 0xFF
            print(x, y)
            if x > 300 and x < 360 and x != -1:
                print('eh')
                if y < 440 and y != -1:
                    print('oh')
                    liigu(-0.4, 9 / 6 * pi, 0, ser)
                    print('aha')

                else:
                    liigu(0, 0, 0, ser)

            else:

                if x < 300 and x != -1:
                    liigu(0, 0, -1, ser)

                elif x > 360 and x != -1:
                    liigu(0, 0, 1, ser)

                else:
                    liigu(0, 0, 0, ser)

        if k == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
    ser.close()
except:
    cv2.destroyAllWindows()
    cap.release()
    ser.close()