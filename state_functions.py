from detection_functions import detector
from movement_functions import liigu, viska, orbit
import time
import math
from time import *
import cv2
import serial

def leia_nurk(x):
    nurk =  -((x - 319) / 319) * math.pi * 0.4
    return nurk

def findBall(ser, detectors, cap, korv, kiirusOtse, kiirusKeera, kiirusPoora, state):
    print("find ball")
    ret, mask, x, y, area, xx = detectors[0].detect(cap)
    ret_k, mask_k, x_k, y_k, area_k, w = detectors[korv].detect(cap)
    cv2.imshow('pall', ret)
    cv2.imshow('korv', ret_k)
    print("findBall", x_k, area_k, basket_dist(w))
    if y < 100:
        y = -1
        x = -1
        area = -1
    if x != -1:
        return 'search and destroy'
    if 290 < x_k < 350 and area_k > 100:
        liigu(-kiirusOtse, 0 * math.pi, 0, ser)
    if x_k < 290 and area_k > 10:
        liigu(0, 0, -kiirusKeera, ser)
    if x_k > 350 and area_k > 10:
        liigu(0, 0, kiirusKeera, ser)
    if x_k < 0 or area_k < 100:
        liigu(0, 0, -kiirusPoora, ser)
    if basket_dist(w) < 65:
        state = 'search and destroy'
    return state



def viskeTugevus(distance):
    offset = 50
    power2 = int(1577 - 1.72 * distance + 0.013 * math.pow(distance, 2) + offset)
    power = int(1263 + 3.51 * distance - math.pow(0.00481, math.pow(distance, 2)) + offset)
    power3 = 0.0063 * math.pow(distance, 2) - 0.9 * distance + 1453 + offset
    print("viske kaugus", distance)
    if(distance < 80):
        print("power", 1580)
        return 1580
    # if(distance > )
    if (power3 > 2100):
        print("power", 2100)
        return 2100
    if (power3 <= 1200):
        print("power", 1400)
        return 1400
    else:
        print("power", power3)
        return power3


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

def check_input(ser, RobotID, FieldID, state):
    #print(ser.readline().decode())
    input = str(ser.readline()).split(':')[-1]
    #print("input: ", input)
    if input != "b''":
        input = input[:-4]
        # print(input)
    print("input: ", input)
    #sleep(1)
    if input == 'a{0}PING-----'.format(RobotID):
        ser.write(("rf:a" + RobotID + "ACK-----\n").encode())
    if input == 'a{0}START----'.format(RobotID):
        print("START~~")
        ser.write(("rf:a" + RobotID + "ACK-----\n").encode())
        delay = time() + 1
        while time() < delay:
            # time()
            liigu(-0.3, 0 * math.pi, 0, ser)
            sleep(0.01)
            # print(delay)
        liigu(0, 0, 0, ser)
        return 'search and destroy'
    if input == 'a{0}STOP-----'.format(RobotID):
        ser.write(("rf:a" + RobotID + "ACK-----\n").encode())
        return 'stop'
    if input == 'a{0}XSTART----\n'.format(FieldID):
        return 'search and destroy'
    if input == 'a{0}XSTOP-----\n'.format(FieldID):
        return 'stop'

    return state


def search_and_destroy(ser, detectors, cap, korv, forwards_speed, rotate_speed, rotate_speed_search, r_d, kontroll, kaugusVasak, kaugusParem, kaugusVasakSuurem, kaugusParemSuurem, shift_speed):
    global rotate_delay
    global liigu_kontroll
    global liigu_aeg

    minArea = 10
    rotate_delay = r_d
    viska(1200, ser)
    # ser.write('fs:0\n'.encode())
    ret, mask, x, y, area, xx = detectors[0].detect(cap)
    ret_k, mask_k, x_k, y_k, area_k, w = detectors[korv].detect(cap)
    # print("korvi kaugus", korviKaugus(y_k))
    # print("wp: ", w)
    # i = focalLenght(w)
    print("kaugus", basket_dist(w))
    cv2.imshow('pall', ret)
    cv2.imshow('korv', ret_k)
    print("pall", x, y, area)
    if y < 100:
        y = -1
        x = -1
        area = -1
    if y > 430 and area >= minArea:
        kontroll = 0
        print("Tagasi")
        liigu(forwards_speed, 0 * math.pi, 0, ser)
    elif y > 380 and kaugusVasak < x < kaugusParem and area >= minArea:
        kontroll = 0
        print('hakkab poorama')
        liigu(0, 0, 0, ser)
        state = 'rotate'
        # cannontime = time()+5

        # liigu(0, 0, 0, ser)
    elif y > 380 and area >= minArea and x < kaugusVasak:
        liigu(-shift_speed, math.pi / 2, 0, ser)

    elif y > 380 and area >= minArea and x > kaugusParem:
        liigu(-shift_speed, -math.pi / 2, 0, ser)

    elif area >= minArea:
        kontroll = 0
        print('pall on keskel')
        if y != -1:
            print('liigub edasi')
            nurk = leia_nurk(x)
            liigu(-forwards_speed, nurk, 0, ser)
            # q = time() + 0.15
            rotate_delay = time() + 2
    elif False:
        if kaugusVasakSuurem < x < kaugusParemSuurem  and area >= minArea:
            kontroll = 0
            print('pall on keskel')
            liigu(0, 0, 0, ser)
            if y != -1:
                print('liigub edasi')
                liigu(-forwards_speed, 0 * math.pi, 0, ser)
                # q = time() + 0.15
                rotate_delay = time() + 2

            else:
                print('else')
                # liigu(0, 0, 0, ser)
                # liigu(-0.4, 9 / 6 * pi, 0, ser)

    else:
        print('else2')
        if False:
            if 0 <= x <= kaugusVasak and area >= minArea:
                kontroll = 0
                print('pall on vasakul')
                liigu(0, 0, -rotate_speed, ser)
                rotate_delay = time() + 4

            elif x >= kaugusParem and area >= minArea:
                kontroll = 0
                print('pall on paremal')
                liigu(0, 0, rotate_speed, ser)
                rotate_delay = time() + 4

        # otsib palli
        elif time() > rotate_delay:
            print('mujal', kontroll)
            kontroll += 1
            if kontroll > 60:
                state = "find ball"
                kontroll = 0
            liigu(0, 0, rotate_speed_search, ser)


        else:
            print('see')
            liigu(0, 0, 0, ser)
    try:
        return state, rotate_delay, kontroll
    except Exception as e:
        print("SAD except:" + str(e))
        return 'search and destroy', rotate_delay, kontroll

def kill_ball(ser, detectors, cap, basket, attack_speed):
    global viska_kontroll
    global viska_aeg
    global liigu_kontroll
    global liigu_aeg
    print("kill ball")
    ret, mask, x, y, area, xx = detectors[0].detect(cap)
    ret_k, mask_k, x_k, y_k, area_k, w = detectors[basket].detect(cap)
    cv2.imshow('pall', ret)
    cv2.imshow('korv', ret_k)
    power = viskeTugevus(basket_dist(w))
    print("power ", power)
    print("kill ball")
    a = time() + 3
    viska(power, ser)

    while time() < a:
        viska(power, ser)
        liigu(-attack_speed, 0 * math.pi, 0, ser)

    state = 'search and destroy'
    return state

def rotate(ser ,detectors, cap, basket, rotate_speed, radius, kaugusVasak, kaugusParem, kaugusVasakSuurem, kaugusParemSuurem):
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
            print("kill ball0")
            state = 'kill ball'
        if x_k < 310 and area_k > 10:
            orbit(radius, -rotate_speed, ser)
            if not (y > 380 and kaugusVasak < x < kaugusParem and area > 80):
                return 'search and destroy'
        if x_k > 330 and area_k > 10:
            orbit(radius, rotate_speed, ser)
            if not (y > 380 and kaugusVasak < x < kaugusParem and area > 80):
                return 'search and destroy'
        # kui ei n'e korvi
        if x_k < 0 or area_k < 100:
            orbit(radius, rotate_speed * 2, ser)
            if not (y > 380 and kaugusVasakSuurem < x < kaugusParemSuurem and area > 80):
                return 'search and destroy'
    except:
        state = 'search and destroy'
        # pass
    try:
        return state
    except:
        return "rotate"