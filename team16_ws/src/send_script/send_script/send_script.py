#!/usr/bin/env python
import rclpy
import cv2
import sys
sys.path.append('/home/robot/colcon_ws/install/tm_msgs/lib/python3.6/site-packages')
from tm_msgs.msg import *
from tm_msgs.srv import *
import time
import math
import numpy as np
from .image_find_dots import FindDots
from .image_find_cup import FindCup

def main(args=None):
    rclpy.init(args=args)

    node = takeAPicture()
    node2 = findCup()

    move(node2.circle_x, node2.circle_y, 300)
    green, red = findPot(node, "glass")
    toPutTeaBagX, toPutTeaBagY = getDivision(green, red, 3, 5)
    getTeaBag(toPutTeaBagX,toPutTeaBagY)

    PourPot(node, "glass")
    # PourPot(node, "metal")

def findPot(node, material):
    for green, red in zip(node.green, node.red):
        dist = math.sqrt((green[0]-red[0])**2 + (green[1]-red[1])**2)
        if (material == "glass" || material == "all") and dist >= 130 and dist < 150:
            print("#################################################")
            print("glass", green, red)
            print("#################################################")
            material = "glass"
            return Calibrate(green, red, material)
        elif (material == "metal" || material == "all") and dist >= 170 and dist < 200:
            print("#################################################")
            print("metal", green, red)
            print("#################################################")
            material = "metal"
            return Calibrate(green, red, material)

def PourPot(node, material):
    move_h = 300.0
    grab_h = 300.0
    release_h = 125.0
    rx, ry, ra = 300.0, 300.0, 90.0
    handle, tip = findPot(node, material)
    _open()
    endX, endY, endZ, l, deltaX, deltaY = lieDownAndGrab(tip[0], tip[1], handle[0], handle[1], material)
    Pouring(endX,endY,endZ,200,deltaX,deltaY)

def lieDownAndGrab(startX,startY,endX,endY,material="metal"):
    if material == "metal":
        grabH = 104.5 # 54 on floor
    elif material == "glass":
        grabH = 58
    moveH = 300
    deltaX, deltaY = endX - startX, endY - startY
    theta = 180 + (90.00 + Atan(deltaX,deltaY))
    move(endX, endY, moveH, -180, 0, 135, 0)
    move(endX, endY, moveH, -90, 180, 135, 0)
    move(endX, endY, moveH, -90, 180, theta, 0)
        
    l = 170 if material == "metal" else 130 if material == "glass" else 0
    endX += l*deltaX/math.sqrt(deltaX**2+deltaY**2)
    endY += l*deltaY/math.sqrt(deltaX**2+deltaY**2)
    
    move(endX, endY, moveH, -90, 180, theta, 0)
    move(endX, endY, grabH+50, -90, 180, theta) # go down
    move(endX, endY, grabH, -90, 180, theta)
    
    lengthTowardTeaPot = 25
    endX -= (deltaX/abs(deltaX)) * lengthTowardTeaPot * abs(math.sin(theta*math.pi/180))
    endY -= (deltaY/abs(deltaY)) * lengthTowardTeaPot * abs(math.cos(theta*math.pi/180))

    move(endX, endY, grabH, -90, 180, theta)
    _close()

    endZ = 250
    time.sleep(5)
    move(endX, endY, endZ, -90, 180, theta) # grab
    time.sleep(5)
    move(endX, endY, endZ, -90, 180, 225)
    return endX,endY,endZ,l,deltaX,deltaY

def Pouring(endX=200,endY=400,endZ=170,l=200,deltaX=100,deltaY=-100,pouringTheta=45,SAMPLE_POINTS=4):
    theta = -90
    l = 205
    # endX += l*deltaX/math.sqrt(deltaX**2+deltaY**2)
    # endY += l*deltaY/math.sqrt(deltaX**2+deltaY**2)
    move(endX,endY,endZ,-90,180,225)
    deltaTh = pouringTheta
    deltaZ = math.sin(deltaTh*math.pi/180)*l*1.1
    deltaXY = (1-math.cos(deltaTh*math.pi/180))*l/math.sqrt(2)
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

def getTeaBag(placeX=230,placeY=230):
    # stick about place
    # move(330,550,100,-180,0,135)              

    # teabagshome about place
    # move(175,605,167,-180,0,135)
    global step
    startX, startY = 175, 605
    height = 167
    oneStepSize = 12.5
    distance = step*oneStepSize
    if step == 1:   distance += 5
    toX, toY = startX + distance, startY + distance
    avoidHitHeight = 500
    forword = 20
    placeHeight = 400
    theta = 40  # degree

    move(startX,startY,height+100,-180,0,135)   # position 1 : preparing to grab tea bag
    move(startX,startY,height,-180,0,135)       # preparing to grab tea bag
    move(toX,toY,height,-180,0,135)             # position 2 : foward into line
    height += 100
    move(toX,toY,height,-180,0,135)             # position 2 : foward into line
    move(toX,toY,height,-180,0,135)             # position 3 : upward
    move(toX,toY,height,-180,0,135)             # position 4 : preparing to grab tea bag
    move(toX,toY,height,-180,0,135)             # position 5 : preparing to grab tea bag

    move(placeX,placeY,avoidHitHeight,-180,0,135)
    move(placeX,placeY,placeHeight,-180,0,135)
    move(placeX+forword,placeY+forword,placeHeight,-180,0,135)
    move(placeX+forword,placeY+forword,placeHeight,-180+theta,0,135)
    step += 1
#-------------constants---------------
targetP1 = "230, 230, 730, -180, 0, 135.00"
photoTarget = "230, 230, 700, -180, 0, 135.00"
step = 1
#---------------tools-----------------
def getDivision(dot1,dot2,weight1,weight2):
    totalWeight = weight1 + weight2
    return (dot1[0]*weight1+dot2[0]*weight2)/totalWeight, (dot1[1]*weight1+dot2[1]*weight2)/totalWeight

def Calibrate(x, y, material):
    heightScaleMap = {
        "metal": 0.8,
        "glass": 0.885,
        None: 0.885
    }
    scale = heightScaleMap[material]
    newx = (x-288)*scale + 285
    newy = (y-285)*scale + 285
    return newx, newy

def takeAPicture(material=None):
    moveTo(photoTarget)
    send_script("Vision_DoJob(job1)")
    cv2.waitKey(1)
    node = FindDots('find_dots',material)
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
