from detection_functions import detector
from movement_functions import liigu
from math import pi
from time import time
import cv2
import serial
import time


port = 'COM4'

ser = serial.Serial(
    port=port,
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS,
    timeout=0
)

#try:
FieldID = 'B'
RobotID = FieldID + 'D'



cv2.namedWindow("kontroll")
time.sleep(1)
print('n')




while True:
    k = cv2.waitKey(5) & 0xFF
    input = str(ser.readline()).split(':')[-1]
    if input != "b''":
        input = input[:-4]
        print(input)
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

    if k == 27:
        break
print('n')

cv2.destroyAllWindows()
ser.close()
#except:
#    cv2.destroyAllWindows()
#    ser.close()