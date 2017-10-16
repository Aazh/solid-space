import serial
import cv2
from rattakiirus import wheelCalc, mainboardSpeedCalc
from math import pi

ser = serial.Serial(
    port='3',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS
)

if ser.isOpen():
    print("Ühendus loodud")

    i = 0
    j = 0
    speed = 0
    angle = 0 * pi
    angularVelocity = 0
    while True:
        cv2.namedWindow("kontroll")
        k = cv2.waitKey(30) & 0xFF
        if k == ord("w"):
            angle = 0 * pi
            speed = 0.1
            angularVelocity = 0
            i = 0
        elif k == ord("a"):
            angle = 1 / 2 * pi
            speed = 0.1
            angularVelocity = 0
            i = 0
        elif k == ord("s"):
            angle = 1 * pi
            speed = 0.1
            angularVelocity = 0
            i = 0
        elif k == ord("d"):
            angle = 3 / 2 * pi
            speed = 0.1
            angularVelocity = 0
            i = 0
        elif k == ord("q"):
            angle = 0
            speed = 0
            angularVelocity = 0.5
        elif k == ord("e"):
            angle = 0
            speed = 0
            angularVelocity = -0.5
        else:
            if i == 5:
                speed = 0
                angle = 0 * pi
                angularVelocity = 0
            i += 1
        if k == 27:
            break

        j += 1
        if j > 5:
            j = 0
            wheelSpeed0 = str(mainboardSpeedCalc(wheelCalc(0, speed, angle, angularVelocity)))
            wheelSpeed1 = str(mainboardSpeedCalc(wheelCalc(1, speed, angle, angularVelocity)))
            wheelSpeed2 = str(mainboardSpeedCalc(wheelCalc(2, speed, angle, angularVelocity)))

            #ser.write("sg\n".encode())
            ser.write("sd"+wheelSpeed0+";"+wheelSpeed1+";"+wheelSpeed2+"\n").encode()

            #time.sleep(1)
            #while ser.inWaiting() > 0:
            #    vastus = ser.readline().decode("utf-8")
            #    print("got: " + vastus)



    ser.close()

else:
    print("Ühenduse loomine ebaõnnestus!")