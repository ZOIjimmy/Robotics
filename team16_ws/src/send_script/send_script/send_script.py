#!/usr/bin/env python
# from rclpy.node import Node

'''
TODO_LIST
4. accuracy problem (from graph, from calculation)
'''

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
    lieDownAndGrab(tip[0], tip[1], handle[0], handle[1], material)

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
    move(endX, endY, grabH, -90, 180, theta)
    time.sleep(5)

    # grab
    _close()
    time.sleep(5)
    move(endX, endY, 250, -90, 180, theta)
    time.sleep(5)
    potlength = 70
    endX += potlength*deltaX/math.sqrt(deltaX**2+deltaY**2)
    endY += potlength*deltaY/math.sqrt(deltaX**2+deltaY**2)
    move(endX, endY, 250, -90, 180, theta)
    move(endX, endY, 400, -90, 180, theta)
    time.sleep(5)
    move(endX, endY, 400, -40, 180, theta)
    time.sleep(5)
    _open()
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
        sleep(1)

def takeAPicture():
    moveTo(photoTarget)
    _open()
    send_script("Vision_DoJob(job1)")
    cv2.waitKey(1)
    return ImageSub('image_sub')

def main(args=None):
    rclpy.init(args=args)

    # constants
    targetP1 = "230, 230, 730, -180, 0, 135.00"
    photoTarget = "230, 230, 700, -180, 0, 135.00"
    release_h = 100.0
    object_h = 25.0
    offsetX, offsetY = 0 , 0
    stack = []

    _open()
    node = takeAPicture()
    rclpy.spin_once(node)

    # pour pot
    print(node.blue, node.red, node.green)
    for blue in node.blue:
        for red in node.red:
            dist = math.sqrt((blue[0]-red[0])**2 + (blue[1]-red[1])**2)
            print("dist",dist)
            if dist >= 200 and dist <= 250:
                # metal one
                PourPot(blue, red, "metal")
                return
            if dist >= 100 and dist < 200:
                # glass one
                PourPot(blue, red, "glass")
                return 

    # assignment4

    # for area, ox, oy, oa in zip(node.areas, node.oxs, node.oys, node.oas):
    #     if  area >= 1000 and area <= 5000:
    #         StackCube(ox+offsetX, oy+offsetY, oa, release_h)
    #         release_h += object_h

    returnForFree()
    _open()
    # rclpy.shutdown()

if __name__ == '__main__':
    main()
