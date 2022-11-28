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

def move(x, y, z, a, grip=-1):
    target = "%f, %f, %f, -180.00, 0.0, %f" % (x, y, z, a)
    script = "PTP(\"CPP\","+target+",100,200,0,false)"
    send_script(script)
    if grip >= 1: _close()
    elif grip >= 0: _open()
    time.sleep(1)

def moveWithPot(x, y, z, a, b, c):
    target = "%f, %f, %f, %f, %f, %f" % (x, y, z, a, b, c)
    script = "PTP(\"CPP\","+target+",100,200,0,false)"
    send_script(script)
    _close()
    time.sleep(1)

def PourPot(ox, oy, oa):
    move_h = 300.0
    grab_h = 125.0
    pour_h = 200.0
    release_h = 125.0

    ra = 90.0
    rx = 300.0
    ry = 300.0

    ox += something * math.cos(oa)
    oy += something * math.sin(oa)

    move(ox, oy, move_h, oa, 0.0)
    
    # TODO fill the angles to grab the pot
    a = 123
    b = 456

    moveWithPot(ox, oy, grab_h, a, b, oa)
    moveWithPot(ox, oy, move_h, a, b, oa)
    # TODO not sure how it works. maybe need to change ra
    moveWithPot(rx, ry, move_h, a, b, ra)
    moveWithPot(rx, ry, pour_h, a, b, ra)

    # TODO pour water may be very buggy
    t = 0 # loop
    l = 1234 # length from gripper to tip of the pot
    mx, my, mz, ma, mb = rx, ry, pour_h, a, b
    for i in range(t):
        moveWithPot(mx, my, mz, ma, mb, ra)
        mx += math.cos(ra) * l
        my += math.sin(ra) * l
        mz += 1
        # TODO
        ma += 1234
        mb += 1234

    moveWithPot(rx, ry, pour_h, a, b, ra)
    moveWithPot(rx, ry, move_h, a, b, ra)
    moveWithPot(ox, oy, move_h, a, b, oa)
    moveWithPot(ox, oy, release_h, a, b, oa)
    
    _open()
    time.sleep(1)

    move(rx, ry, move_h, ra)

def StackCube(ox, oy, oa, release_h):
    move_h = 300.0
    grab_h = 105.0

    ra = 90.0
    rx = 300.0
    ry = 300.0

    move(ox, oy, move_h, oa, 0)
    move(ox, oy, grab_h, oa, 1)
    move(ox, oy, move_h, ra)
    move(rx, ry, move_h, ra)
    move(rx, ry, release_h, ra, 0)
    move(rx, ry, move_h, ra)

##

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



'''
    can grip place : targetP2 = "200.00, 350, 50, -270.00, 0.0, 45.00"
'''

'''
    +50 -50 +150->+200 -40 setTo40 setTo45
'''

def moveToTarget(x,y,z,a,b,c):
    target = "{}, {}, {}, {}, {}, {}".format(str(x),str(y),str(z),str(a),str(b),str(c))
    script = "PTP(\"CPP\","+target+",100,200,0,false)"
    send_script(script)
    return

def moveToTakePhotoPlace():
    moveToTarget(230,230,700,-180,0,135)


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
    targetP1 = "230, 230, 730, -180, 0, 135.00"


    _open()
    moveToTakePhotoPlace()

    send_script("Vision_DoJob(job1)")
    cv2.waitKey(1)

    node = ImageSub('image_sub')
    rclpy.spin_once(node)


    release_h = 105.0
    object_h = 25.0


    for ox, oy, oa in zip(node.oxs, node.oys, node.oas):
        StackCube(ox, oy, oa, release_h)
        release_h += object_h
        

    moveToTakePhotoPlace()




    # _open()
    
    # moveToTarget(0,350,60,-270,0,90)
    # _close()

    # time.sleep(10)

    # moveToTarget(400,300,400,-270,0,45)

    # moveToTarget(400,300,400,-230,0,45)





# What does Vision_DoJob do? Try to use it...

# -------------------------------------------------
#     send_script("Vision_DoJob(job1)")
#     cv2.waitKey(1)
# #--------------------------------------------------
#     node = ImageSub('image_sub')
#     rclpy.spin(node)

    # script = "PTP(\"CPP\","+targetP1+",100,200,0,false)"
    # send_script(script)
    # set_io(0.0)# 1.0: close gripper, 0.0: open gripper

    #rclpy.shutdown()

if __name__ == '__main__':
    main()
