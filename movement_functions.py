from math import pi, cos
from time import time
import serial

wheelConfig0 = [11/6*pi , 0.135]
wheelConfig1 = [1/6*pi , 0.135]
wheelConfig2 = [6/6*pi , 0.135]

def wheelCalc(wheel, robotSpeed, robotDirectionAngle, robotAngularVelocity):
    wheelConfig = [wheelConfig0, wheelConfig1, wheelConfig2]
    wheelAngle = wheelConfig[wheel][0]
    wheelDistanceFromCenter = wheelConfig[wheel][1]
    wheelLinearVelocity = robotSpeed * cos(robotDirectionAngle - wheelAngle) + wheelDistanceFromCenter * robotAngularVelocity
    return wheelLinearVelocity


gearboxReductionRatio = 18.75
encoderEdgesPerMotorRevolution = 64
wheelRadius = 0.035
pidControlFrequency = 60
timer = 0.5

def mainboardSpeedCalc(wheelLinearVelocity):
    wheelAngularVelocity = wheelLinearVelocity / wheelRadius
    wheelSpeedToMainboardUnits = gearboxReductionRatio * encoderEdgesPerMotorRevolution / (
    2 * pi * wheelRadius * pidControlFrequency)
    wheelAngularSpeedMainboardUnits = wheelLinearVelocity * wheelSpeedToMainboardUnits
    return int(wheelAngularSpeedMainboardUnits)

def liigu(speed, angle, angularVelocity, ser):
    global liigu_kontroll
    global liigu_aeg
    wheelSpeed0 = str(mainboardSpeedCalc(wheelCalc(0, speed, angle, angularVelocity)))
    wheelSpeed1 = str(mainboardSpeedCalc(wheelCalc(1, speed, angle, angularVelocity)))
    wheelSpeed2 = str(mainboardSpeedCalc(wheelCalc(2, speed, angle, angularVelocity)))
    liigu_uus = "sd:{0}:{1}:{2}\n".format(wheelSpeed0, wheelSpeed1, wheelSpeed2).encode()
    try:
        if liigu_uus == liigu_kontroll:
            if time() > liigu_aeg:
                liigu_aeg = time() + timer
                print('k')
                ser.write(liigu_uus)
                print('b')
        else:
            liigu_aeg = time() + timer
            liigu_kontroll = liigu_uus
            print('k')
            ser.write(liigu_uus)
            print('b')
    except Exception as e:
        print("Liigu except:" + str(e))
        liigu_aeg = time() + timer
        liigu_kontroll = liigu_uus
        print('k')
        ser.write(liigu_uus)
        print('b')

def rotation(speed, ser):
    global liigu_kontroll
    global liigu_aeg
    wheelSpeed0 = str(mainboardSpeedCalc(speed*0.1))
    wheelSpeed1 = str(mainboardSpeedCalc(speed*0.1))
    wheelSpeed2 = str(mainboardSpeedCalc(speed))
    liigu_uus = "sd:{0}:{1}:{2}\n".format(wheelSpeed0, wheelSpeed1, wheelSpeed2).encode()
    try:
        if liigu_uus == liigu_kontroll:
            if time() > liigu_aeg:
                liigu_aeg = time() + timer
                print('k')
                ser.write(liigu_uus)
                print('b')
        else:
            liigu_aeg = time() + timer
            liigu_kontroll = liigu_uus
            print('k')
            ser.write(liigu_uus)
            print('b')
    except Exception as e:
        print("rotation except:" + str(e))
        liigu_aeg = time() + timer
        liigu_kontroll = liigu_uus
        print('k')
        ser.write(liigu_uus)
        print('b')

def viska(x, ser):
    global viska_kontroll
    global viska_aeg
    viska_uus = 'd:{0}\n'.format(x).encode()
    try:
        if viska_uus == viska_kontroll:
            if time() > viska_aeg:
                viska_aeg = time() + timer
                ser.write(viska_uus)
        else:
            viska_aeg = time() + timer
            viska_kontroll = viska_uus
            ser.write(viska_uus)
    except Exception as e:
        print("viska except:" + str(e))
        viska_aeg = time() + timer
        viska_kontroll = viska_uus
        ser.write(viska_uus)