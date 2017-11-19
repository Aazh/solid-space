from detection_functions import detector
from movement_functions import liigu, viska, orbit

import math
from time import *
import cv2
import serial


def viskeTugevus(distance):
    offset = -100
    power = int(1263 + 3.51 * distance - math.pow(0.00481, math.pow(distance, 2)) + offset)
    if (distance > 250):
        print("power", 2200)
        return 2200
    # if(distance > )
    if (power > 1400):
        print("power", power)
        return power
    else:
        print("power", 1400)
        return 1400


def basket_dist(widthP):
    width = 16
    focal = 525
    return (width * focal) / widthP


def focalLenght(widthP):
    width = 16  # cm
    distance = 100
    print("pixlid ", widthP)
    print("Focal: ", ((widthP * distance) / width))
    return ((widthP * distance) / width)
    # 525

def check_input(ser, RobotID, FieldID):
    global state
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

def search_and_destroy(ser, detectors, cap, basket, forwards_speed, rotate_speed ,r_d):
    global rotate_delay
    global liigu_kontroll
    global liigu_aeg
    rotate_delay = r_d
    viska(1000, ser)
    # ser.write('fs:0\n'.encode())
    ret, mask, x, y, area, xx = detectors[0].detect(cap)
    ret_k, mask_k, x_k, y_k, area_k, w = detectors[basket].detect(cap)
    # print("korvi kaugus", korviKaugus(y_k))
    # print("wp: ", w)
    # i = focalLenght(w)
    print("kaugus", basket_dist(w))
    cv2.imshow('pall', ret)
    cv2.imshow('korv', ret_k)
    print("pall", x, y)
    if y > 380 and 295 < x < 345:
        print('2')
        liigu(0, 0, 0, ser)
        state = 'rotate'
        # cannontime = time()+5

        # liigu(0, 0, 0, ser)
    elif 295 < x < 345:
        print('eh')
        liigu(0, 0, 0, ser)
        if y != -1:
            print('if')
            liigu(-forwards_speed, 0 * math.pi, 0, ser)
            # q = time() + 0.15
            rotate_delay = time() + 2

        else:
            print('else')
            # liigu(0, 0, 0, ser)
            # liigu(-0.4, 9 / 6 * pi, 0, ser)

    else:
        print('else2')
        if x < 300 and x != -1:
            print('siin')
            liigu(rotate_speed, 0, -1, ser)
            rotate_delay = time() + 4

        elif x > 360 and x != -1:
            print('seal')
            liigu(rotate_speed, 0, 1, ser)
            rotate_delay = time() + 4

        # otsib palli
        elif time() > rotate_delay:
            print('mujal')
            liigu(rotate_speed, 0, 1, ser)


        else:
            print('see')
            liigu(0, 0, 0, ser)
    try:
        return state
    except:
        return 'search and destroy'

def kill_ball(ser, detectors, cap, basket, attack_speed):
    global viska_kontroll
    global viska_aeg
    global liigu_kontroll
    global liigu_aeg
    ret, mask, x, y, area, xx = detectors[0].detect(cap)
    ret_k, mask_k, x_k, y_k, area_k, w = detectors[basket].detect(cap)
    cv2.imshow('pall', ret)
    cv2.imshow('korv', ret_k)
    power = viskeTugevus(basket_dist(w))
    print("kill ball")
    a = time() + 3
    viska(power, ser)

    while time() < a:
        # viska(1600, ser)
        liigu(-attack_speed, 0 * math.pi, 0, ser)

    state = 'search and destroy'
    return state

def rotate(ser ,detectors, cap, basket, rotate_speed, radius):
    global liigu_kontroll
    global liigu_aeg
    try:
        ret, mask, x, y, area, xx = detectors[0].detect(cap)
        ret_k, mask_k, x_k, y_k, area_k, w = detectors[basket].detect(cap)

        cv2.imshow('pall', ret)
        cv2.imshow('korv', ret_k)
        # rotation(-0.4, ser)
        print("korv ", x_k, y_k, area_k)
        if 310 < x_k < 330 and area_k > 100 and y > 360 and area > 10:
            state = 'kill ball'
        if x_k < 310 and area_k > 10:
            orbit(radius, -rotate_speed, ser)
        if x_k > 330 and area_k > 10:
            orbit(radius, rotate_speed, ser)
        # kui ei n'e korvi
        if x_k < 0 or area_k < 100:
            orbit(radius, -rotate_speed, ser)
        if not (y > 380 and 280 < x < 360 and area > 80):
            state = 'search and destroy'
    except:
        state = 'search and destroy'
        # pass
    try:
        return state
    except:
        return "rotate"