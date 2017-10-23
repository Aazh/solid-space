from detection_functions import detector
from movement_functions import liigu
from math import pi
from time import time
import cv2
import serial

cap = cv2.VideoCapture(0)
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
q = 0
rotate = time() + 4
try:
    detectors = []
    for i in range(3):
        looker = detector('colorConfig{0}.txt'.format(i), i)
        detectors.append(looker)


    cv2.namedWindow("kontroll")


    while True:
        k = cv2.waitKey(5) & 0xFF

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
            print(x, y)
            if time() < q:
                liigu(-0.4, 9 / 6 * pi, 0, ser)
                rotate = time() + 4
            elif y > 420 and y != -1:
                state = 'kill ball'
                liigu(0, 0, 0, ser)
            elif x > 300 and x < 360 and x != -1:
                print('eh')
                if y < 420 and y != -1:
                    q = time() + 0.15
                    rotate = time() + 4
                    #while time() < q:
                    #    print('k')
                    #liigu(-0.4, 9 / 6 * pi, 0, ser)

                #elif y > 420 and y != -1:
                #    state = 'kill ball'

                else:
                    liigu(0, 0, 0, ser)

            else:

                if x < 300 and x != -1:
                    liigu(0, 0, -1, ser)
                    rotate = time() + 4

                elif x > 360 and x != -1:
                    liigu(0, 0, 1, ser)
                    rotate = time() + 4

                elif time() > rotate:
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