from detection_functions import detector
from movement_functions import liigu, viska, rotation
from state_functions import *

import math
from time import *
import cv2
import serial

korv = 1 #1 lilla, 2 sinine
timer = 0
kiirusPoora = 0.1
kiirusOtse = 0.3
kiirusKeera = 0.6
kiirusRunda = 0.2
kiirusKordaja = 2
#kiirusPoora, kiirusOtse, kiirusKeera, kiirusRunda = kiirusPoora * kiirusKordaja, kiirusOtse * kiirusKordaja, kiirusKeera * kiirusKordaja, kiirusRunda * kiirusKordaja
radius = 0.3
rotate_speed_search = 2

"""def viskeTugevus(distance):
    offset = -100
    power = int(1263+3.51*distance - math.pow(0.00481, math.pow(distance, 2)) + offset)
    if(distance > 200):
        print("power", 2100)
        return 2100
    #if(distance > )
    if(power > 1400):
        print("power", power)
        return power
    else:
        print("power", 1400)
        return 1400"""

def korviKaugus(widthP):
    width = 16
    focal = 525
    return (width* focal) / widthP

def focalLenght(widthP):
    width = 16 #cm
    distance = 100
    print("pixlid ", widthP)
    print("Focal: ", ((widthP * distance) / width))
    return ((widthP * distance) / width)
    #525

def main():
    FieldID = 'A'
    RobotID = FieldID + 'D'
    kontroll = time()
    cap = cv2.VideoCapture(0)
    port = 'COM3'

    ser = serial.Serial(
        port=port,
        baudrate=9600,
        timeout=0.000001,
        write_timeout=0.000001
    )

    print('+++++++++++++++++++++')
    #ser.write("fs:0\n".encode())
    #ser.write('d:1200\n'.encode())
    #sleep(5)
    #ser.write("fs:1\n".encode())
    print('OK')
    t = time() + 2
    #state = 'stop'
    state = 'search and destroy'
    q = 0
    #palli otsimise delay
    rotate_delay = time() + 1
    try:
        detectors = []
        for i in range(3):
            looker = detector('colorConfig{0}.txt'.format(i), i)
            detectors.append(looker)


        cv2.namedWindow("pall")
        cv2.namedWindow("korv")





        while True:
            #print(ser.readline().decode())
            state = check_input(ser, RobotID, FieldID, state)
            print("check input")
            k = cv2.waitKey(5) & 0xFF
            print("State?")
            if state == 'search and destroy':
                print("State: ", state)
                state, rotate_delay = search_and_destroy(ser, detectors, cap, korv, kiirusOtse, kiirusKeera, rotate_speed_search, rotate_delay, 0)

            elif state == 'kill ball':
                print("State: ", state)
                state = kill_ball(ser, detectors, cap, korv, kiirusRunda)

            elif state == 'rotate':
                print("State: ", state)
                state = rotate(ser, detectors, cap, korv, kiirusPoora, radius)
            elif state == 'find ball':
                print("State: ", state)
                state = findBall(ser, detectors, cap, korv, kiirusOtse, kiirusPoora, state)
            else:
                print("STOP!!")


            if k == 27:
                break

        cv2.destroyAllWindows()
        cap.release()
        liigu(0, 0, 0, ser)
        ser.close()

    except Exception as e:
        print("main except:" + str(e))
        #print('except')
        cv2.destroyAllWindows()
        cap.release()
        liigu(0, 0, 0, ser)
        ser.close()

if __name__ == '__main__':
    main()