#!/usr/bin/env python
from .image_find_dots import FindDots
from .image_find_cup import FindCup
from tm_msgs.msg import *
from tm_msgs.srv import *
import numpy as np
import socket
import rclpy
import time
import math
import cv2
import sys
sys.path.append('/home/robot/colcon_ws/install/tm_msgs/lib/python3.6/site-packages')
sys.path.append('/home/robot/workspace2/team16_ws/src/send_script/send_script')
sys.path.append('/home/robot/workspace2/team16_ws/src/send_script/send_script/yolov7')
from .cup_height_prediction import predictCupHeight
from yolov7.detect_realsense import detect_with_opt
import serial
import time

from .sensor_data_read import getHeightData, turnAngle, resetTurnAngle, giveSugar

from .height_sensor import calculateTurnAngle

def main(args=None):
    rclpy.init(args=args)

    # Connection
    # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client.connect(('140.112.30.40', 13751))
    # order = eval(str(client.recv(1024), encoding='utf-8'))

    # take a picture at photoTarget
    node = takeAPicture()

    # find tools
    # tools = findTool(node)

    # find glass teapot
    # green, red = findPot(node, "glass")

    # Cup Detection and Height Prediction
    # cup_x, cup_y, cup_z_cm, cup_r = cupDetectionHeightPred()

    # height sensor
    # turnHeightSensor(cup_x, cup_y)

    # # get central of the glass teapot
    # toPutTeaBagX, toPutTeaBagY = getDivision(green, red, 2.2, 7)

    # # put the teabag to the central of the glass teapot
    # #getTeaBag(tools[2][0],tools[2][1],toPutTeaBagX,toPutTeaBagY)
    
    # targetTeaPot = toPutTeaBagX, toPutTeaBagY, 200
    # #PourPot(node, "metal", targetTeaPot)

    # targetCup = cup_x, cup_y, cup_z_cm*16
    # PourPot(node,"glass",targetCup)

    # pour out teabag
    # garbageCollection(green, red)

    # # addSugar(stickPositionX, stickPositionY, targetX, targetY, pourHeight)
    # addSugar(tools[0][0], tools[0][1], cup_x, cup_y, cup_z_cm*10 + 100)

    # #stir(tools[1], (cup_x,cup_y,160,cup_r))

    # # PourPot(node,"milk",(230,230,300))            !!!!!cannot use now !!!!!

def garbageCollection(handle, tip):
    sifterx, siftery = getDivision(handle,tip,2.2,7)
    endX,endY,endZ,l,deltaX,deltaY = lieDownAndGrab(sifterx, siftery, handle[0], handle[1], "sifter")
    theta = 180 + (90.00 + Atan(deltaX,deltaY))
    move(endX-130, endY+130, endZ, -90, 180, theta)
    move(endX-130, endY+130, endZ, -90, 0, theta)
    move(endX-130, endY+130, endZ, -90, 180, theta)
    move(endX, endY, endZ, -90, 180, theta)
    move(endX, endY, 158, -90, 180, theta)
    move(endX, endY, 108, -90, 180, theta)
    _open()

def stir(tool, cup):
    getStirStick(tool[0],tool[1])
    stirring(cup[0],cup[1],cup[2],cup[3])
    putBackStirStick(tools[0],tools[1])

def turnHeightSensor(cup_x, cup_y):
    turn_angle = calculateTurnAngle(cup_x, cup_y)
    time.sleep(5)
    print("turn_angle", turn_angle)
    resetTurnAngle(ser)
    time.sleep(5)
    turnAngle(ser, turn_angle)
    time.sleep(3)
    h = getHeightData(ser)
    print(h)

def cupDetectionHeightPred():
    time.sleep(3)
    resetTurnAngle(ser)
    # Cup Detection and Height Prediction
    x1, y1, x2, y2 = detect_with_opt()
    AABB_height_in_pixel = y2 - y1

    findcup_node = findCup()
    cup_center_world_x, cup_center_world_y = findcup_node.circle_x, findcup_node.circle_y
    move(cup_center_world_x, cup_center_world_y, 700, -180, 0, 135.00)
    parallel_dis_to_origin = (cup_center_world_x - cup_center_world_y)/(2**0.5) + cup_center_world_y * (2**0.5)
    print(parallel_dis_to_origin)

    cup_height = predictCupHeight(cup_center_world_x, cup_center_world_y, AABB_height_in_pixel)
    print("cup_height:", cup_height)
    new_cup_x, new_cup_y = CalibrateCupPosition(cup_center_world_x, cup_center_world_y, cup_height)
    return new_cup_x, new_cup_y, cup_height, findcup_node.circle_r

distMap = {"metal": (215, 245), "glass": (150, 180), "milk": (40, 58)}
def findPot(node, material):
    tool_reds = findTool(node)
    for green in node.green:
        for red in node.red:
            if tool_reds != None and red in tool_reds: continue    
            dist = math.sqrt((green[0]-red[0])**2 + (green[1]-red[1])**2)
            print("distance:",dist)
            if dist >= distMap[material][0] and dist < distMap[material][1]:
                print('#'*50, "\nglass", green, red, '\n', '#'*50)
                a = Calibrate(green[0], green[1], material)
                b = Calibrate(red[0], red[1], material)
                return a, b
    print("oops glass")
    exit(1)
    return None, None

tools = None
def findTool(node):
    tool_reds = []
    for red in node.red:
        x , y = red
        if y - x > 250 or y - x < -100 : continue
        if x + y < 600 or x + y > 900 : continue
        tool_reds.append(red)
    if len(tool_reds) < 3:
        print("tool_reds", tool_reds)
        print("ERROR")
        return None

    a = tool_reds[0][0] - tool_reds[0][1]
    b = tool_reds[1][0] - tool_reds[1][1]
    c = tool_reds[2][0] - tool_reds[2][1]

    if a < b:
        tool_reds[0], tool_reds[1] = tool_reds[1], tool_reds[0]
        a, b = b, a
    if b < c:
        tool_reds[1], tool_reds[2] = tool_reds[2], tool_reds[1]
        b, c = c, b
    if a < b:
        tool_reds[0], tool_reds[1] = tool_reds[1], tool_reds[0]
        a, b = b, a

    return tool_reds       # [left,mid,right]

heightMap = {"metal": 104.5, "glass": 58, "milk": 76 ,"sugarPlate": 230, "sifter":108}
lengthMap = {"metal": 170, "glass": 128, "milk": 130, "sifter": 88}
def PourPot(node, material, target):
    handle, tip = findPot(node, material)
    _open()

    endX, endY, endZ, l, deltaX, deltaY = lieDownAndGrab(tip[0], tip[1], handle[0], handle[1], material)
    original_position = [handle[0],handle[1],heightMap[material]]

    if material == "metal":
        Pouring(target[0],target[1],target[2],315,material,deltaX,deltaY)
    elif material == "glass":
        Pouring(target[0],target[1],target[2],240,material,deltaX,deltaY)
    elif material == "milk":
        Pouring(target[0],target[1],target[2],130,material,deltaX,deltaY)

    moveBackAfterPouring(original_position,material)

def lieDownAndGrab(startX,startY,endX,endY,material="metal"):
    grabH = heightMap[material]
    
    moveH = 350
    deltaX, deltaY = endX - startX, endY - startY
    theta = 180 + (90.00 + Atan(deltaX,deltaY))
    move(endX, endY, moveH, -180, 0, 135, 0)
    move(endX, endY, moveH, -90, 0, theta, 0)
    move(endX, endY, moveH, -90, 180, theta, 0)

    l = lengthMap[material]
    endX += l*deltaX/math.sqrt(deltaX**2+deltaY**2)
    endY += l*deltaY/math.sqrt(deltaX**2+deltaY**2)
    
    move(endX, endY, moveH, -90, 180, theta, 0)
    move(endX, endY, grabH+50, -90, 180, theta) # go down
    move(endX, endY, grabH, -90, 180, theta)
    
    lengthTowardTeaPot = 25
    endX -= (deltaX/abs(deltaX)) * lengthTowardTeaPot * abs(math.sin(theta*math.pi/180))
    endY -= (deltaY/abs(deltaY)) * lengthTowardTeaPot * abs(math.cos(theta*math.pi/180))

    move(endX, endY, grabH, -90, 180, theta)
    time.sleep(5)
    time.sleep(5)
    _close()        # grab the handle
    time.sleep(5)   # wait and check if successfully grabbed
    time.sleep(5)

    endZ = 250
    move(endX, endY, endZ, -90, 180, theta)         # move upward
    move(endX, endY, endZ, -90, 180, 225)           # turn on XY plane to deg = 225
    return endX,endY,endZ,l,deltaX,deltaY

def Pouring(endX,endY,endZ,l,material,deltaX=100,deltaY=-100,pouringTheta=45,SAMPLE_POINTS=9):
    endX -= l
    endY += l
    move(endX,endY,endZ + 150,-90,180,225)          # avoid hitting something -> first move higher
    move(endX,endY,endZ,-90,180,225)                # move downward

    if material == "metal":
        l = 340
        SAMPLE_POINTS = 2
    elif material == "glass":
        l = 280
        SAMPLE_POINTS = 9
    else:
        l = 0
        SAMPLE_POINTS = 0

    theta = -90
    deltaTh = pouringTheta
    deltaXY = (1-math.cos(deltaTh*math.pi/180))*l/math.sqrt(2)*1.2
    deltaZ = math.sin(deltaTh*math.pi/180)*l*0.95
    for j in range(SAMPLE_POINTS):
        i = j + 1
        endX += (deltaXY / SAMPLE_POINTS)
        endY -= (deltaXY / SAMPLE_POINTS)
        endZ += (deltaZ / SAMPLE_POINTS)
        theta += (deltaTh / SAMPLE_POINTS)
        move(endX,endY,endZ,theta,180,225)

    # after for loop the teapot should have same performance as below line
    # move(endX+deltaXY,endY-deltaXY,endZ+deltaZ,-90+deltaTh,180,225)   

    # wait and then turn to place teapot horizontally
    time.sleep(5)

    for j in range(2):
        i = j + 1
        endX -= (deltaXY / SAMPLE_POINTS)
        endY += (deltaXY / SAMPLE_POINTS)
        endZ -= (deltaZ / SAMPLE_POINTS)
        theta -= (deltaTh / SAMPLE_POINTS)
        move(endX,endY,endZ,theta,180,225)
    move(endX,endY,400,-90,180,225)
    return

    '''
    _open()
    move(endX, endY, moveH, -180, 0, 135, 0)
    time.sleep(5)
    move(endX, endY, moveH, -90, 180, 135, 0)
    move(endX, endY, moveH, -270.00, 0.0, 180 + (90.00 + Atan(deltaX,deltaY)), 0)
    move(endX, endY, grabH, -270.00, 0.0, 180 + (90.00 + Atan(deltaX,deltaY)))
    _close()
    move(endX, endY, moveH, -270.00, 0.0, 180 + (90.00 + Atan(deltaX,deltaY)))
    '''

def moveBackAfterPouring(original_position,material):
    # put down the teapot and then open
    length = lengthMap[material]*0.9
    original_position[0] -= length/(2**0.5)
    original_position[1] += length/(2**0.5)

    move(original_position[0],original_position[1],400,-90,180,225)
    move(original_position[0],original_position[1],original_position[2],-90,180,225)
    _open()
    move(original_position[0]+2,original_position[1]-2,original_position[2],-90,180,225)
    move(original_position[0]-2,original_position[1]+2,original_position[2],-90,180,225)
    move(original_position[0],original_position[1],original_position[2],-90,180,225)

    # move backward to leave the teapot handle
    backward = 50
    original_position[0] -= backward
    original_position[1] += backward
    
    move(original_position[0],original_position[1],original_position[2],-90,180,225)
    move(original_position[0],original_position[1],400,-90,180,225)

def findCup():
    findCupPhotoTargetPt = np.array([400, -100])
    photoTargetPt = np.array([230, 230])
    deltaVec = findCupPhotoTargetPt - photoTargetPt
    print(deltaVec)
    findCupPhotoTarget = str(findCupPhotoTargetPt[0]) + ", " + str(findCupPhotoTargetPt[1]) + ", 700, -180, 0, 135.00"
    moveTo(findCupPhotoTarget)
    send_script("Vision_DoJob(job1)")
    cv2.waitKey(1)
    node = FindCup('find_cup', deltaVec)
    rclpy.spin_once(node)
    return node

def getTeaBag(toolX, toolY, placeX=230,placeY=230):
    # stick about place
    # move(330,550,100,-180,0,135)              

    # teabagshome about place
    # move(175,605,167,-180,0,135)
    global step
    startX, startY = 175, 605
    height = 168
    oneStepSize = 12.5
    distance = step*oneStepSize
    if step == 1:   distance += 5
    toX, toY = startX + distance, startY + distance
    avoidHitHeight = 500
    forword = 20
    placeHeight = 300
    theta = 40  # degree

    stickLength = 30
    placeX -= stickLength
    placeY -= stickLength

    _open()
    move(toolX,toolY,avoidHitHeight,-180,0,135) 
    move(toolX,toolY,170,-180,0,135) 
    move(toolX,toolY,100,-180,0,135) 
    time.sleep(5)
    _close()
    time.sleep(5)
    move(toolX,toolY,170,-180,0,135) 
    move(toolX,toolY,avoidHitHeight,-180,0,135)

    move(startX,startY,avoidHitHeight,-180,0,135)   # position 1 : preparing to grab tea bag
    move(startX,startY,height+70,-180,0,135)
    move(startX,startY,height,-180,0,135)           #              move straight downward
    move(toX,toY,height,-180,0,135)                 # position 2 : foward into line
    move(toX,toY,height+70,-180,0,135)
    move(toX,toY,avoidHitHeight,-180,0,135)         #              move straight upward

    move(placeX,placeY,avoidHitHeight,-180,0,135)
    move(placeX,placeY,placeHeight,-180,0,135)

    # first move forward and then pour
    move(placeX+forword,placeY+forword,placeHeight,-180,0,135)
    move(placeX+forword,placeY+forword,placeHeight,-180+theta,0,135)
    step += 1

    move(placeX+forword,placeY+forword,placeHeight)
    move(placeX+forword,placeY+forword,avoidHitHeight)
    move(toolX,toolY,avoidHitHeight)
    move(toolX,toolY,200)
    move(toolX,toolY,100)
    _open()

    move(toolX,toolY,avoidHitHeight)

def addSugar(stickPositionX, stickPositionY, targetX, targetY, pourHeight):
    getSugarPlate(stickPositionX,stickPositionY)
    getSugar(8)
    pourSugar(targetX, targetY, pourHeight)
    putBackSugarPlate(stickPositionX, stickPositionY)

def getSugarPlate(positionX, positionY):
    avoidHeight = 400
    grabH = 118
    _open()

    a,b,c = -180,0,-45
    move(positionX,positionY,avoidHeight)
    move(positionX,positionY,grabH+100)
    move(positionX,positionY,grabH+100,a,b,c)       # turn the joint

    move(positionX,positionY,grabH,a,b,c)
    time.sleep(3)
    move(positionX,positionY,grabH,a,b,c)
    time.sleep(3)
    move(positionX,positionY,grabH,a,b,c)

    _close()
    move(positionX,positionY,grabH,a,b,c)
    time.sleep(3)

    move(positionX,positionY,grabH+70,a,b,c)
    move(positionX,positionY,avoidHeight,a,b,c)
    move(positionX,positionY,avoidHeight,-180,0,225)
    time.sleep(3)
    return 

def getSugar(count):
    global ser
    move(410,550,235,-180,0,225)
    time.sleep(3)
    move(600,360,235,-180,0,225)
    time.sleep(3)
    time.sleep(3)
    _open()
    time.sleep(3)
    time.sleep(3)
    for i in range(count):
        giveSugar(ser)
    move(410,550,235,-180,0,225)
    move(300,300,350)

    moveH = 130
    theta = 225
    move(300, 300, moveH+200, -90, 180, theta, 0)
    move(410, 550, moveH+200, -90, 180, theta)
    move(510, 450, moveH+200, -90, 180, theta)
    move(510, 450, moveH, -90, 180, theta)
    move(528, 432, moveH, -90, 180, theta)

    time.sleep(3)
    time.sleep(3)
    _close()        # grab the handle
    time.sleep(3)   # wait and check if successfully grabbed
    time.sleep(3)

    move(410,550,150,-90,180,225)
    move(410,550,300,-90,180,225)
    return

def pourSugar(centroidX, centroidY, pourHeight):
    #             pour-> 180~0 (deg)
    move(300,300,400,-90,180,225)
    
    offset1 = 225
    centroidX -= offset1 / 2**(1/2)
    centroidY += offset1 / 2**(1/2)

    # offset2 = 15
    # centroidX -= offset2
    # centroidY -= offset2
    move(centroidX, centroidY, 400,-90,180,225)
    move(centroidX, centroidY, pourHeight,-90,180,225)
    
    for i in range(10):
        move(centroidX, centroidY, pourHeight,-90,180-(i+1)*18,225)
    
    move(centroidX, centroidY, pourHeight,-90,90,225)
    move(centroidX, centroidY, pourHeight,-90,180,225)

def putBackSugarPlate(positionX, positionY):
    # change back grab state
    move(230,230,500,-90,180,225)
    move(330,630,400,-90,180,225)
    move(330,630,300,-90,180,225)
    move(430,530,300,-90,180,225)
    move(430,530,132,-90,180,225)
    move(530,430,132,-90,180,225)

    time.sleep(5)
    _open()
    time.sleep(5)

    move(300,300,400,-90,180,225)
    move(300,300,400)
    move(410,550,235)
    move(410,550,235,-180,0,225)
    move(580,380,235,-180,0,225)
    move(610,350,235,-180,0,225)
    
    time.sleep(5)
    _close()
    time.sleep(5)

    move(580,380,235,-180,0,225)
    move(410,550,235,-180,0,225)
    move(230,230,700)

    avoidHeight = 400
    grabH = 118
    a,b,c = -180,0,-45

    move(positionX,positionY,avoidHeight)
    move(positionX,positionY,avoidHeight,a,b,c)
    move(positionX,positionY,grabH+70,a,b,c)
    move(positionX,positionY,grabH,a,b,c)

    time.sleep(5.0)
    move(positionX,positionY,grabH,a,b,c)
    time.sleep(5.0)
    _open()

    time.sleep(5.0)
    move(positionX,positionY,grabH,a,b,c)
    time.sleep(5.0)

    move(positionX,positionY,grabH,a,b,c)
    move(positionX,positionY,grabH+70,a,b,c)
    move(positionX,positionY,avoidHeight,a,b,c)
    move(positionX,positionY,avoidHeight)
    move(230,230,700)
    return

def getStirStick(positionX, positionY):
    avoidHeight = 400
    grabH = 100
    a,b,c = -180,0,-45

    _open()
    move(positionX,positionY,avoidHeight)
    move(positionX,positionY,grabH+100)
    move(positionX,positionY,grabH+100,a,b,c)

    move(positionX,positionY,grabH,a,b,c)
    time.sleep(5.0)
    move(positionX,positionY,grabH,a,b,c)
    time.sleep(5.0)
    move(positionX,positionY,grabH,a,b,c)
    time.sleep(5.0)
    move(positionX,positionY,grabH,a,b,c)
    time.sleep(3.0)
    _close()
    time.sleep(3.0)

    move(positionX,positionY,grabH,a,b,c)
    move(positionX,positionY,grabH+70,a,b,c)
    move(positionX,positionY,avoidHeight,a,b,c)
    move(positionX,positionY,avoidHeight)
    time.sleep(5)
    return 

def putBackStirStick(positionX, positionY):
    move(230,230,700)
    avoidHeight = 400
    grabH = 100
    a,b,c = -180,0,-45

    move(positionX,positionY,avoidHeight)
    move(positionX,positionY,avoidHeight,a,b,c)
    move(positionX,positionY,grabH+70,a,b,c)
    move(positionX,positionY,grabH,a,b,c)

    time.sleep(5.0)
    _open()
    time.sleep(5.0)
    
    move(positionX,positionY,grabH,a,b,c)
    move(positionX,positionY,grabH+70,a,b,c)
    move(positionX,positionY,avoidHeight,a,b,c)
    move(positionX,positionY,avoidHeight)
    move(230,230,700)
    return 

def stirring(centroidX,centroidY,stirHeight,radius,turns=5):
    # reset stirring radius
    radius = 13
    a,b,c = 90,0,120
    avoidHeight = 300
    offset =  120   # gripper length = 12cm

    move(230,230,700)
    move(230,230,350,90,0,45)
    move(230,230,350,90,0,c)

    centroidX -= abs(offset*math.cos(30/180*math.pi))
    centroidY -= abs(offset*math.sin(30/180*math.pi))

    move(centroidX,centroidY,350,a,b,c)
    # move to the stirring position
    move(centroidX,centroidY,stirHeight+avoidHeight,a,b,c)
    move(centroidX,centroidY,stirHeight+70,a,b,c)
    move(centroidX,centroidY,stirHeight,a,b,c)
    time.sleep(5)

    for _ in range(turns):
        move(centroidX+radius,centroidY+radius,stirHeight,a,b,c)
        move(centroidX-radius,centroidY+radius,stirHeight,a,b,c)
        move(centroidX-radius,centroidY-radius,stirHeight,a,b,c)
        move(centroidX+radius,centroidY-radius,stirHeight,a,b,c)
    move(centroidX,centroidY,stirHeight,a,b,c)          
    move(centroidX,centroidY,stirHeight+70,a,b,c)          
    time.sleep(5)

    # leave the cup
    move(centroidX,centroidY,stirHeight+avoidHeight,a,b,c)      
    move(230,230,350,a,b,c)
    move(230,230,350,90,0,45)
    move(230,230,700)
    return

#-------------constants---------------
targetP1 = "230, 230, 730, -180, 0, 135.00"
photoTarget = "230, 230, 700, -180, 0, 135.00"
step = 1
ser = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_55736303631351118190-if00', timeout=1)
#---------------tools-----------------
def getDivision(dot1,dot2,weight1,weight2):
    totalWeight = weight1 + weight2
    return (dot1[0]*weight1+dot2[0]*weight2)/totalWeight, (dot1[1]*weight1+dot2[1]*weight2)/totalWeight

def Calibrate(x, y, material=None):
    heightScaleMap = {
        "metal": 0.8,
        "glass": 0.885,
        "milk": 0.81,
        "ground": 1,
        None: 1
    }
    scale = heightScaleMap[material]
    newx = (x-288)*scale + 288
    newy = (y-285)*scale + 285
    return newx, newy

def CalibrateCupPosition(x, y, height_in_cm):
    heightScale = 1- height_in_cm * 10 / 575
    scale = heightScale
    newx = (x- (400 + 58))*scale + (400 + 58)
    newy = (y-(-100 + 55))*scale + (-100 + 55)
    return newx, newy

def takeAPicture():
    _open()
    moveTo(photoTarget)
    send_script("Vision_DoJob(job1)")
    cv2.waitKey(1)
    node = FindDots('find_dots')
    rclpy.spin_once(node)
    return node

def _open():
    set_io(0.0)

def _close():
    set_io(1.0)

def move(x, y, z, a=-180, b=0, c=135, g=-1):
    target = "%f, %f, %f, %f, %f, %f" % (x, y, z, a, b, c)
    script = "PTP(\"CPP\","+target+",100,200,0,false)"
    send_script(script)
    if g >= 1: _close()
    elif g >= 0: _open()
    time.sleep(2)

def moveTo(target):
    script = "PTP(\"CPP\","+target+",100,200,0,false)"
    send_script(script)

def Atan(deltaX, deltaY):
    return math.atan(deltaY/deltaX) * 180 / math.pi

def set_io(state):
    gripper_node = rclpy.create_node('gripper')
    gripper_cli = gripper_node.create_client(SetIO, 'set_io')

    while not gripper_cli.wait_for_service(timeout_sec=1.0):
        gripper_node.get_logger().info('service not availabe, waiting again...')
    
    io_cmd = SetIO.Request()
    io_cmd.module = 1
    io_cmd.type = 1
    io_cmd.pin = 0
    io_cmd.state = state
    gripper_cli.call_async(io_cmd)
    gripper_node.destroy_node()

def send_script(script):
    arm_node = rclpy.create_node('arm')
    arm_cli = arm_node.create_client(SendScript, 'send_script')

    while not arm_cli.wait_for_service(timeout_sec=1.0):
        arm_node.get_logger().info('service not availabe, waiting again...')

    move_cmd = SendScript.Request()
    move_cmd.script = script
    arm_cli.call_async(move_cmd)
    arm_node.destroy_node()
'''---------------notes-----------------
    can grip place : targetP2 = "200.00, 350, 50, -270.00, 0.0, 45.00"
    +50 -50 +150->+200 -40 setTo40 setTo45

    xShouldMove = abs(lengthTowardTeaPot*math.cos(Atan(deltaX,deltaY)))
    yShouldMove = abs(lengthTowardTeaPot*math.sin(Atan(deltaX,deltaY)))
    endX -= (deltaX/abs(deltaX))*xShouldMove
    endX -= (deltaY/abs(deltaY))*yShouldMove
    if deltaX > 0:
        endX -= abs(lengthTowardTeaPot*math.cos(Atan(deltaX,deltaY)))
    else:
        endX += abs(lengthTowardTeaPot*math.cos(Atan(deltaX,deltaY)))
    if deltaY > 0:
        endY -= abs(lengthTowardTeaPot*math.sin(Atan(deltaX,deltaY)))
    else:
        endY += abs(lengthTowardTeaPot*math.sin(Atan(deltaX,deltaY))    )
    endX -= lengthTowardTeaPot*deltaX/math.sqrt(deltaX**2+deltaY**2)
    endY -= lengthTowardTeaPot*deltaY/math.sqrt(deltaX**2+deltaY**2)

    pour template
    potlength = 70
    endX += potlength*deltaX/math.sqrt(deltaX**2+deltaY**2)
    endY += potlength*deltaY/math.sqrt(deltaX**2+deltaY**2)
    move(endX, endY, 250, -90, 180, theta)
    move(endX, endY, 400, -90, 180, theta)
    time.sleep(5)
    move(endX, endY, 400, -40, 180, theta)
    time.sleep(5)

    move(endX+deltaXY/SAMPLE_POINTS*i,endY-deltaXY/SAMPLE_POINTS*i,280,-90,180,225)
    move(endX+deltaXY/SAMPLE_POINTS*i,endY-deltaXY/SAMPLE_POINTS*i,280,-60,180,225)
    move(endX+deltaXY,endY-deltaXY,150+deltaZ,-60,180,225)

    green dots
    move(350, 250, 58, -90, 180, 45) #583.66 451.88
    move(400, 50, 58, -90, 180, 45) #998.5 700.0
    move(250, 300, 58, -90, 180, 45) #337.5 538.0

    move(350,350,54,-90,180,225)  # metal teapot can grab
    move(0,500,104.5,-90,180,225)  # metal teapot can grab (on the heating plate)
----------------useless----------------'''
def assignment4():
    release_h = 100.0
    object_h = 25.0
    for area, ox, oy, oa in zip(node.areas, node.oxs, node.oys, node.oas):
        if  area >= 1000 and area <= 5000:
            StackCube(ox, oy, oa, release_h)
            release_h += object_h
    rclpy.shutdown()

def StackCube(ox, oy, oa, release_h):
    move_h = 300.0
    grab_h = 125.0
    rx, ry, ra = 300.0, 300.0, 90.0
    move(ox, oy, move_h, c=oa, g=0)
    move(ox, oy, grab_h, c=oa, g=1)
    move(ox, oy, move_h, c=ra)
    move(rx, ry, move_h, c=ra)
    move(rx, ry, release_h, c=ra, g=0)
    move(rx, ry, move_h, c=ra)
#---------------main--------------------
if __name__ == '__main__':
    main()