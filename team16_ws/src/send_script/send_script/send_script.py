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

def PourPot(handle, tip):
    move_h = 300.0
    grab_h = 300.0
    release_h = 125.0
    rx, ry, ra = 300.0, 300.0, 90.0

'''
    can grip place : targetP2 = "200.00, 350, 50, -270.00, 0.0, 45.00"
'''

'''
    +50 -50 +150->+200 -40 setTo40 setTo45
'''
    _open()
    lieDownAndGrab(tip[0], tip[1], handle[0], handle[1])
    move(rx, ry, move_h, -270, 0, ra)

    # TODO

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

def Atan(deltaX, deltaY):
    return math.atan(deltaY/deltaX) * 180 / math.pi

def lieDownAndGrab(startX,startY,endX,endY):
    # moveTo("230, 230, 700, -180, 0, 135.00")    # insurance
    grabH = 200
    moveH = 300
    deltaX, deltaY = endX - startX, endY - startY
    move(endX, endY, moveH, -270.00, 0.0, 180 + (90.00 + Atan(deltaX,deltaY)), 0)
    move(endX, endY, grabH, -270.00, 0.0, 180 + (90.00 + Atan(deltaX,deltaY)))
    _close()
    move(endX, endY, moveH, -270.00, 0.0, 180 + (90.00 + Atan(deltaX,deltaY)))

def takeAPicture():
    moveTo(photoTarget)
    _open()
    send_script("Vision_DoJob(job1)")
    cv2.waitKey(1)
    return ImageSub('image_sub')

def main(args=None):
    rclpy.init(args=args)

    #--- move command by joint angle ---#
    # script = 'PTP(\"JPP\",45,0,90,0,90,0,35,200,0,false)'

    #--- move command by end effector's pose (x,y,z,a,b,c) ---#
    # targetP1 = "398.97, -122.27, 748.26, -179.62, 0.25, 90.12"s

    # Initial camera position for taking image (Please do not change the values)
    # For right arm: targetP1 = "230.00, 230, 730, -180.00, 0.0, 135.00"
    # For left  arm: targetP1 = "350.00, 350, 730, -180.00, 0.0, 135.00"

    # paras  =   x,   y ,  z ,up2dow down2right  rotate joint
    # constants
    targetP1 = "230, 230, 730, -180, 0, 135.00"
    photoTarget = "230, 230, 700, -180, 0, 135.00"
    release_h = 100.0
    object_h = 25.0
    offsetX, offsetY = 0 , 0

    # _open()
    # moveTo("200.00, 350, 350, -270.00, 0.0, 45.00")
    # moveTo("200.00, 350, 93, -270.00, 0.0, 45.00")
    # _close()
    # moveTo("200.00, 350, 250, -270.00, 0.0, 45.00")
    # moveTo("200.00, 350, 250, -270.00, 180.0, 45.00")

    # moveTo("200.00, 350, 300, -270.00, 0.0, 45.00")
    # time.sleep(8)
    # moveTo("200.00, 350, 160, -270.00, 0.0, 45.00")
    # _close()
    # moveTo("200.00, 350, 93, -270.00, 0.0, 45.00")

    node = takeAPicture()
    rclpy.spin_once(node)

    # pour pot
    
    for blue in node.blue:
        for red in node.red:
            dist = sqrt((blue[0]-red[0])**2 + (blue[1]-red[1])**2)
            if dist >= 430 and dist <= 450:
                # metal one
                PourPot(blue, red)

    # assignment4

    # for area, ox, oy, oa in zip(node.areas, node.oxs, node.oys, node.oas):
    #     if  area >= 1000 and area <= 5000:
    #         StackCube(ox+offsetX, oy+offsetY, oa, release_h)
    #         release_h += object_h

    # moveTo(targetP1)
    # _open()

    #rclpy.shutdown()

if __name__ == '__main__':
    main()
