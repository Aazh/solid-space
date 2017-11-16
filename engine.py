from detection_functions import detector


from movement_functions import liigu, viska, rotation
import math
from time import *
import cv2
import serial
korv = 2 #1 lilla, 2 sinine
timer = 0
kiirusPoora = 0.1
kiirusOtse = 0.4
kiirusKeera = 0.1
kiirusRunda = 0.4
def viskeTugevus(distance):
    offset = -100
    power = int(1263+3.51*distance - math.pow(0.00481, math.pow(distance, 2)) + offset)
    if(distance > 250):
        print("power", 2200)
        return 2200
    #if(distance > )
    if(power > 1400):
        print("power", power)
        return power
    else:
        print("power", 1400)
        return 1400
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

    cap = cv2.VideoCapture(0)
    port = 'COM3'

    ser = serial.Serial(
        port=port,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        dsrdtr=True,
        timeout=0,
        write_timeout=1
    )

    print('+')
    #ser.write("fs:0\n".encode())
    ser.write('d:1200\n'.encode())
    #sleep(5)
    #ser.write("fs:1\n".encode())
    print('OK')
    t = time() + 2
    #state = 'stop'
    state = 'search and destroy'
    q = 0
    #palli otsimise delay
    rotate = time() + 1
    try:
        detectors = []
        for i in range(3):
            looker = detector('colorConfig{0}.txt'.format(i), i)
            detectors.append(looker)


        cv2.namedWindow("pall")
        cv2.namedWindow("korv")

        delay = time()
        while True:
            input = str(ser.readline()).split(':')[-1]
            print("input: ", input)
            if input != "b''":
                input = input[:-4]
                # print(input)
            if input == 'a{0}PING-----'.format(RobotID):
                ser.write("rf:a{0}ACK------\n".format(RobotID).encode())
            if input == 'a{0}START----'.format(RobotID):
                ser.write("rf:a{0}ACK------\n".format(RobotID).encode())
                state = 'search and destroy'
            if input == 'a{0}STOP-----'.format(RobotID):
                ser.write("rf:a{0}ACK------\n".format(RobotID).encode())
                state = 'stop'
            if input == 'a{0}XSTART----\n'.format(FieldID):
                state = 'search and destroy'
            if input == 'a{0}XSTOP-----\n'.format(FieldID):
                state = 'stop'
            input = None


            k = cv2.waitKey(5) & 0xFF

            if state == 'search and destroy':
                viska(1000, ser)
                #ser.write('fs:0\n'.encode())
                ret, mask, x, y, area, xx = detectors[0].detect(cap)
                ret_k, mask_k, x_k, y_k, area_k, w = detectors[korv].detect(cap)
                #print("korvi kaugus", korviKaugus(y_k))
                #print("wp: ", w)
                #i = focalLenght(w)
                print("kaugus", korviKaugus(w))
                #ret, mask, x, y, area = detectors[0].detect(cap)
                cv2.imshow('pall', ret)
                cv2.imshow('korv', ret_k)
                print("pall", x, y)
                #if time() < q:
                #    print('1')
                #    liigu(-0.4, 9 / 6 * pi, 0, ser)
                #    rotate = time() + 4
                if y > 380 and 295 < x < 345:
                    print('2')
                    liigu(0, 0, 0, ser)
                    state = 'rotate'
                    #cannontime = time()+5

                    #liigu(0, 0, 0, ser)
                elif 295 < x < 345:
                    print('eh')
                    liigu(0, 0, 0, ser)
                    if y != -1:
                        print('if')
                        liigu(-kiirusOtse, 9 / 6 * math.pi, 0, ser)
                        #q = time() + 0.15
                        rotate = time() + 2

                    else:
                        print('else')
                        #liigu(0, 0, 0, ser)
                        #liigu(-0.4, 9 / 6 * pi, 0, ser)

                else:
                    print('else2')
                    if x < 300 and x != -1:
                        print('siin')
                        liigu(kiirusKeera, 0, -1, ser)
                        rotate = time() + 4

                    elif x > 360 and x != -1:
                        print('seal')
                        liigu(kiirusKeera, 0, 1, ser)
                        rotate = time() + 4

                    #otsib palli
                    elif time() > rotate:
                        print('mujal')
                        liigu(kiirusKeera, 0, 1, ser)


                    else:
                        print('see')
                        liigu(0, 0, 0, ser)



            elif state == 'kill ball':
                ret, mask, x, y, area, xx = detectors[0].detect(cap)
                ret_k, mask_k, x_k, y_k, area_k, w = detectors[korv].detect(cap)
                cv2.imshow('pall', ret)
                cv2.imshow('korv', ret_k)
                power = viskeTugevus(korviKaugus(w))
                print("kill ball")
                a = time() + 3
                viska(power, ser)

                while time() < a:
                    #viska(1600, ser)
                    liigu(-kiirusRunda, 9 / 6 * math.pi, 0, ser)

                state = 'search and destroy'


            elif state == 'rotate':
                try:
                    ret, mask, x, y, area, xx = detectors[0].detect(cap)
                    ret_k, mask_k, x_k, y_k, area_k, w = detectors[korv].detect(cap)

                    cv2.imshow('pall', ret)
                    cv2.imshow('korv', ret_k)
                    # rotation(-0.4, ser)
                    print("korv ", x_k, y_k, area_k)
                    if 310 < x_k < 330 and area_k > 100 and y > 360 and area > 10:
                        state = 'kill ball'
                    if x_k < 310 and area_k > 10:
                        rotation(-kiirusPoora, ser)
                    if x_k > 330 and area_k > 10:
                        rotation(kiirusPoora, ser)
                    #kui ei n'e korvi
                    if x_k < 0 or area_k < 100:
                        rotation(-kiirusPoora, ser)
                    if not (y > 380 and 280 < x < 360 and area > 80):
                        state = 'search and destroy'
                except:
                    state = 'search and destroy'
                    #pass



            print(state)

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