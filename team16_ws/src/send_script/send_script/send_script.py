#!/usr/bin/env python
# from rclpy.node import Node

import rclpy
import cv2
import sys
sys.path.append('/home/robot/colcon_ws/install/tm_msgs/lib/python3.6/site-packages')
from tm_msgs.msg import *
from tm_msgs.srv import *
import time
# from sensor_msgs.msg import Image
# import cv_bridge
import math
import numpy as np
from .image_sub import ImageSub
from .image_find_dots import FindDots
from .image_find_cup import FindCup

photoTarget = "230, 230, 700, -180, 0, 135.00"
stack = []

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
    time.sleep(1)
    stack.append(target)

def PourPot(handle, tip, material):
    move_h = 300.0
    grab_h = 300.0
    release_h = 125.0
    rx, ry, ra = 300.0, 300.0, 90.0

        # can grip place : targetP2 = "200.00, 350, 50, -270.00, 0.0, 45.00"
        # +50 -50 +150->+200 -40 setTo40 setTo45

    _open()
    endX, endY, endZ, l, deltaX, deltaY = lieDownAndGrab(tip[0], tip[1], handle[0], handle[1], material)
    Pouring(endX,endY,endZ,200,deltaX,deltaY)

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

def send_script(script):
    arm_node = rclpy.create_node('arm')
    arm_cli = arm_node.create_client(SendScript, 'send_script')

    while not arm_cli.wait_for_service(timeout_sec=1.0):
        arm_node.get_logger().info('service not availabe, waiting again...')

    move_cmd = SendScript.Request()
    move_cmd.script = script
    arm_cli.call_async(move_cmd)
    arm_node.destroy_node()

# gripper client
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


def moveTo(target):
    script = "PTP(\"CPP\","+target+",100,200,0,false)"
    send_script(script)
    stack.append(target)

def Atan(deltaX, deltaY):
    return math.atan(deltaY/deltaX) * 180 / math.pi

def lieDownAndGrab(startX,startY,endX,endY,material):
    # moveTo("230, 230, 700, -180, 0, 135.00")    # insurance
    
    if material == "metal":
        grabH = 61
    elif material == "glass":
        grabH = 40

    # for test
    grabH = 150
    # for test

    moveH = 300
    deltaX, deltaY = endX - startX, endY - startY
    move(endX, endY, moveH, -180, 0, 135, 0)
    time.sleep(5)
    move(endX, endY, moveH, -90, 180, 135, 0)

    deltaX, deltaY = endX-startX, endY-startY
    theta = 180 + (90.00 + Atan(deltaX,deltaY))
    move(endX, endY, moveH, -90, 180, theta, 0)

    time.sleep(5)
    l = 115                                                           +5    #+5: 3Dpinrt
    endX += l*deltaX/math.sqrt(deltaX**2+deltaY**2)
    endY += l*deltaY/math.sqrt(deltaX**2+deltaY**2)
    move(endX, endY, moveH, -90, 180, theta, 0)

    # go down
    move(endX, endY, grabH+50, -90, 180, theta)
    move(endX, endY, grabH, -90, 180, theta, 1)
    print("closing\n")
    time.sleep(5)

    endZ = 250

    # grab
    time.sleep(5)
    move(endX, endY, endZ, -90, 180, theta)
    time.sleep(5)

    move(endX, endY, endZ, -90, 180, 225)
    return  endX,endY,endZ,l,deltaX,deltaY

    ''' pour template
    potlength = 70
    endX += potlength*deltaX/math.sqrt(deltaX**2+deltaY**2)
    endY += potlength*deltaY/math.sqrt(deltaX**2+deltaY**2)
    move(endX, endY, 250, -90, 180, theta)
    move(endX, endY, 400, -90, 180, theta)
    time.sleep(5)
    move(endX, endY, 400, -40, 180, theta)
    time.sleep(5)
    '''
    

def Pouring(endX=200,endY=400,endZ=170,l=200,deltaX=100,deltaY=-100,pouringTheta=45,SAMPLE_POINTS=4):
    # endX, endY = 200, 400
    # endZ = 170
    theta = -90
    # deltaX, deltaY = 100, -100
    l = 200                                                          +5    #+5: 3Dpinrt
    # endX += l*deltaX/math.sqrt(deltaX**2+deltaY**2)
    # endY += l*deltaY/math.sqrt(deltaX**2+deltaY**2)
    move(endX,endY,endZ,-90,180,225)
    deltaTh = pouringTheta
    deltaZ = math.sin(deltaTh*math.pi/180)*l                        *1.1
    deltaXY = (1-math.cos(deltaTh*math.pi/180))*l/math.sqrt(2)
    print(deltaTh,deltaXY,deltaZ)
    for j in range(SAMPLE_POINTS):
        i = j + 1
        endX += (deltaXY/SAMPLE_POINTS)
        endY -= (deltaXY/SAMPLE_POINTS)
        endZ += (deltaZ/SAMPLE_POINTS)
        theta += (deltaTh/SAMPLE_POINTS)
        print("theta",theta)
        move(endX,endY,endZ,theta,180,225)
    # move(endX+deltaXY,endY-deltaXY,endZ+deltaZ,-90+deltaTh,180,225)
    time.sleep(2)
    move(endX,endY,endZ,-90,180,225)



    # _open()
    # move(endX, endY, moveH, -180, 0, 135, 0)
    # time.sleep(5)
    # move(endX, endY, moveH, -90, 180, 135, 0)
    # move(endX, endY, moveH, -270.00, 0.0, 180 + (90.00 + Atan(deltaX,deltaY)), 0)
    # move(endX, endY, grabH, -270.00, 0.0, 180 + (90.00 + Atan(deltaX,deltaY)))
    # _close()
    # move(endX, endY, moveH, -270.00, 0.0, 180 + (90.00 + Atan(deltaX,deltaY)))


def returnForFree():
    for i in range(len(stack)):
        moveTo(stack[-i])
        time.sleep(1)

def takeAPicture():
    moveTo(photoTarget)
    # _open()
    send_script("Vision_DoJob(job1)")
    cv2.waitKey(1)
    node = FindDots('find_dots')
    rclpy.spin_once(node)
    return node

def findCup():
    # findCupPhotoTargetPt = np.array([500, -160])
    findCupPhotoTargetPt = np.array([400, -100])
    photoTargetPt = np.array([230, 230])
    deltaVec = findCupPhotoTargetPt - photoTargetPt
    print(deltaVec)
    findCupPhotoTarget = str(findCupPhotoTargetPt[0]) + ", " + str(findCupPhotoTargetPt[1]) + ", 700, -180, 0, 135.00"
    moveTo(findCupPhotoTarget)
    _open()
    send_script("Vision_DoJob(job1)")
    cv2.waitKey(1)
    node = FindCup('find_cup', deltaVec)
    rclpy.spin_once(node)
    return node

step = 1
def getTeaBag(placeX=230,placeY=230):
    global step

    startX, startY = 100, 500
    height = 160

    oneStepSize = 30
    distance = step*oneStepSize
    toX, toY = startX + distance, startY + distance

    avoidHitHeight = 500

    forword = 20
    placeHeight = 300

    theta = 40  # degree

    move(startX,startY,height,-180,0,135)                            # position 1 : preparing to grab tea bag

    move(toX,toY,height,-180,0,135)            # position 2 : foward into line

    move(toX,toY,height,-180,0,135)            # position 3 : upward

    move(toX,toY,height,-180,0,135)            # position 4 : preparing to grab tea bag

    move(toX,toY,height,-180,0,135)            # position 5 : preparing to grab tea bag


    move(placeX,placeY,avoidHitHeight,-180,0,135)
    move(placeX,placeY,placeHeight,-180,0,135)
    move(placeX+forword,placeY+forword,placeHeight,-180,0,135)
    move(placeX+forword,placeY+forword,placeHeight,-180+theta,0,135)

    step += 1
    return 


def main(args=None):
    rclpy.init(args=args)

    # constants
    targetP1 = "230, 230, 730, -180, 0, 135.00"
    photoTarget = "230, 230, 700, -180, 0, 135.00"
    release_h = 100.0
    object_h = 25.0
    offsetX, offsetY = 0 , 0
    stack = []

    # time.sleep(2)

        # move(endX+deltaXY/SAMPLE_POINTS*i,endY-deltaXY/SAMPLE_POINTS*i,280,-90,180,225)
        # move(endX+deltaXY/SAMPLE_POINTS*i,endY-deltaXY/SAMPLE_POINTS*i,280,-60,180,225)

    # move(endX+deltaXY,endY-deltaXY,150+deltaZ,-60,180,225)


    # _open()

    _close()
    # node = findCup()
    # print(node.circle_x,node.circle_y)

    circleX , circleY = 381.08205 , 100.73405000000002
    
    node = takeAPicture()

    # lieDownAndGrab(200,400,300,300,"glass")
    # getTeaBag()

    # Pouring(endX=circleX,endY=circleY)
    # move(circleX,circleY,170,-90,180,225)


    # # pour pot
    # print(node.blue, node.red, node.green)
    # GREEN, RED, DIST = None, None, None
    # for green in node.green:
    #     for red in node.red:
    #         dist = math.sqrt((green[0]-red[0])**2 + (green[1]-red[1])**2)
    #         print("dist",dist)
    #         if dist >= 100 and dist < 180:
    #             # glass one
    #             PourPot(green, red, "glass")
    #             # GREEN = green
    #             # RED = red
    #             # DIST = dist
    #             break
    
    # node = findCup()

    # move(node.circle_x,node.circle_y,300)
    

    # print(GREEN,RED,DIST)

    # assert GREEN != None

    # toPutTeaBagX, toPutTeaBagY = RED[0]*0.7 + GREEN[0]*0.3, RED[1]*0.7 + GREEN*0.3

    # getTeaBag(toPutTeaBagX,toPutTeaBagY)

    # moveTo(photoTarget)

    # Pouring(GREEN,RED,"glass")



    # assignment4

    # for area, ox, oy, oa in zip(node.areas, node.oxs, node.oys, node.oas):
    #     if  area >= 1000 and area <= 5000:
    #         StackCube(ox+offsetX, oy+offsetY, oa, release_h)
    #         release_h += object_h

    # returnForFree()
    # _open()
    # rclpy.shutdown()

if __name__ == '__main__':
    main()
