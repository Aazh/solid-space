from detection_functions import detector


from movement_functions import liigu, viska, rotation
from math import pi
from time import *
import cv2
import serial

def main():

    FieldID = 'B'
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
    ser.write('d:1000\n'.encode())
    t = time() + 2
    #state = 'stop'
    state = 'rotate'
    q = 0
    rotate = time() + 4
    try:
        detectors = []
        for i in range(3):
            looker = detector('colorConfig{0}.txt'.format(i), i)
            detectors.append(looker)


        cv2.namedWindow("kontroll")


        while True:
            """input = str(ser.readline()).split(':')[-1]
            if input != "b''":
                input = input[:-4]
                #print(input)
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
            input = None"""



            k = cv2.waitKey(5) & 0xFF

            if state == 'search and destroy':

                '''if t < time():
                    t = time() + 2
                    ser.close()
                    ser = serial.Serial(
                        port=port,
                        baudrate=115200,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_TWO,
                        bytesize=serial.EIGHTBITS
                    )'''
                #ser.write('fs:0\n'.encode())

                cv2.imshow('kontroll', ret)ret, mask, x, y, area = detectors[0].detect(cap)
                print(x, y)
                #if time() < q:
                #    print('1')
                #    liigu(-0.4, 9 / 6 * pi, 0, ser)
                #    rotate = time() + 4
                if y > 420 and x > 300 and x < 360:
                    print('2')
                    state = 'kill ball'
                    #cannontime = time()+5

                    #liigu(0, 0, 0, ser)
                elif x > 300 and x < 360 and x != -1 and area > 50:
                    print('eh')
                    if y < 420 and y != -1:
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
                ret_k, mask_k, x_k, y_k, area_k = detectors[1].detect(cap)
                if 300 > x_k > 360:
                    state = 'execute ball'
                a = time() + 2
                viska(1400, ser)
                while time() < a:
                    liigu(-0.2, 9 / 6 * pi, 0, ser)

                state = 'search and destroy'
            else:
                viska(1000, ser)
            print(state)

            if state == 'rotate':
                rotation(0.1, ser)

            if k == 27:
                break

        cv2.destroyAllWindows()
        cap.release()
        liigu(0, 0, 0, ser)
        ser.close()
    except:
        print('except')
        cv2.destroyAllWindows()
        cap.release()
        liigu(0, 0, 0, ser)
        ser.close()



if __name__ == '__main__':
    main()