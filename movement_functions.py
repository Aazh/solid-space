from math import pi, cos
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

def mainboardSpeedCalc(wheelLinearVelocity):
    wheelAngularVelocity = wheelLinearVelocity / wheelRadius
    wheelSpeedToMainboardUnits = gearboxReductionRatio * encoderEdgesPerMotorRevolution / (
    2 * pi * wheelRadius * pidControlFrequency)
    wheelAngularSpeedMainboardUnits = wheelLinearVelocity * wheelSpeedToMainboardUnits
    return int(wheelAngularSpeedMainboardUnits)

def liigu(speed, angle, angularVelocity):
    wheelSpeed0 = str(mainboardSpeedCalc(wheelCalc(0, speed, angle, angularVelocity)))
    wheelSpeed1 = str(mainboardSpeedCalc(wheelCalc(1, speed, angle, angularVelocity)))
    wheelSpeed2 = str(mainboardSpeedCalc(wheelCalc(2, speed, angle, angularVelocity)))

    ser.write("sd:{0}:{1}:{2}:0\n".format(wheelSpeed0, wheelSpeed1, wheelSpeed2).encode())