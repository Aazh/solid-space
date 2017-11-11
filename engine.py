from detection_functions import detector


from movement_functions import liigu, viska, rotation
from math import pi
from time import *
import cv2
import serial

def main():

    FieldID = 'A'
    RobotID = FieldID + 'D'

    cap = cv2.VideoCapture(0)
    port = 'COM3'

    ser = serial.Serial(
        port=port,
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS,
        timeout=0
    )
    print('+')
    #ser.write("fs:0\n".encode())
    ser.write('d:1000\n'.encode())
    #sleep(5)
    #ser.write("fs:1\n".encode())
    print('OK')
    t = time() + 2
    #state = 'stop'
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
            input = str(ser.readline()).split(':')[-1]
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
            if input == 'a{0}XSTART----'.format(FieldID):
                state = 'search and destroy'
            if input == 'a{0}XSTOP-----'.format(FieldID):
                state = 'stop'
            input = None


            k = cv2.waitKey(5) & 0xFF

            if state == 'search and destroy':

                """if t < time():
                    t = time() + 2
                    ser.close()
                    ser = serial.Serial(
                        port=port,
                        baudrate=115200,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_TWO,
                        bytesize=serial.EIGHTBITS
                    )"""
                #ser.write('fs:0\n'.encode())


                ret, mask, x, y, area = detectors[0].detect(cap)
                cv2.imshow('kontroll', ret)
                print(x, y)
                #if time() < q:
                #    print('1')
                #    liigu(-0.4, 9 / 6 * pi, 0, ser)
                #    rotate = time() + 4
                if y > 400 and 300 < x < 360:
                    print('2')
                    state = 'rotate'
                    #cannontime = time()+5

                    #liigu(0, 0, 0, ser)
                elif 300 < x < 360 and area > 50:
                    print('eh')
                    if y < 400 and y != -1:
                        print('if')
                        liigu(-0.4, 9 / 6 * pi, 0, ser)
                        #q = time() + 0.15
                        rotate = time() + 4

                    else:
                        print('else')
                        liigu(0, 0, 0, ser)

                else:
                    print('else2')
                    if x < 300 and x != -1 and area > 10:
                        print('siin')
                        liigu(0, 0, -1, ser)
                        rotate = time() + 4

                    elif x > 360 and x != -1 and area > 10:
                        print('seal')
                        liigu(0, 0, 1, ser)
                        rotate = time() + 4

                    elif time() > rotate:
                        print('mujal')
                        liigu(0, 0, 1, ser)


                    else:
                        print('see')
                        liigu(0, 0, 0, ser)



            if state == 'kill ball':
                print("kill ball")
                a = time() + 3
                viska(1600, ser)
                while time() < a:
                    liigu(-0.2, 9 / 6 * pi, 0, ser)

                state = 'search and destroy'
            else:
                viska(1000, ser)


            if state == 'rotate':
                try:
                    ret, mask, x, y, area = detectors[0].detect(cap)
                    ret_k, mask_k, x_k, y_k, area_k = detectors[2].detect(cap)
                except:
                    pass
                cv2.imshow('kontroll', ret_k)
                rotation(-0.4, ser)
                if 300 < x_k < 360:
                    print('o1')
                if area_k > 100:
                    print('o2')
                if y > 360:
                    print('o3')
                if area > 10:
                    print('o4')
                if 320 < x_k <340 and area_k > 100 and area > 10:
                    state = 'kill ball'
                if y < 400:
                    state = 'search and destroy'


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