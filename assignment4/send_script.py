#!/usr/bin/env python
# from rclpy.node import Node

import rclpy
import cv2
import sys
sys.path.append('/home/robot/colcon_ws/install/tm_msgs/lib/python3.6/site-packages')
from tm_msgs.msg import *
from tm_msgs.srv import *
import time
import math
import numpy as np
from .image_sub import ImageSub

photoTarget = "230, 230, 700, -180, 0, 135.00"
targetP1 = "230.00, 230, 730, -180.00, 0.0, 135.00"

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

def takeAPicture():
    moveTo(photoTarget)
    _open()
    send_script("Vision_DoJob(job1)")
    cv2.waitKey(1)
    return ImageSub('image_sub')

def main(args=None):
    rclpy.init(args=args)

    release_h = 100.0
    object_h = 25.0

    node = takeAPicture()
    rclpy.spin_once(node)

    for area, ox, oy, oa in zip(node.areas, node.oxs, node.oys, node.oas):
        if  area >= 1000 and area <= 10000:
            StackCube(ox+offsetX, oy+offsetY, oa, release_h)
            release_h += object_h

    moveTo(targetP1)
    _open()

    rclpy.shutdown()

if __name__ == '__main__':
    main()
