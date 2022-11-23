#!/usr/bin/env python
from rclpy.node import Node
import rclpy
import cv2
import sys
sys.path.append('/home/robot/colcon_ws/install/tm_msgs/lib/python3.6/site-packages')
from tm_msgs.msg import *
from tm_msgs.srv import *
import time
from sensor_msgs.msg import Image
import cv_bridge
import math
# arm client

def CalcCentroid(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (9, 9), 0)
    img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)[1]
    _, contours, _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cxs, cys, pas = [], [], []
    for c in contours:
        M = cv2.moments(c)
        if M["m00"] >= 1000:
            cx = M["m10"] / M["m00"]
            cy = M["m01"] / M["m00"]
            u20 = M["m20"] / M["m00"] - cx ** 2
            u02 = M["m02"] / M["m00"] - cy ** 2
            u11 = M["m11"] / M["m00"] - cx * cy
            cx = int(cx)
            cy = int(cy)
            cxs.append(cx)
            cys.append(cy)
            pa= 0.5 * math.atan2(2 * u11, u20 - u02)
            pa *= 180 / math.pi
            pas.append(pa)
            gradient=math.tan(pa)
            cv2.circle(img, (cx, cy), 7, (0, 0, 255), -1)
            cv2.line(img, (cx, cy), (cx+300, (cy + int(300*gradient))), (200, 0, 0), 1)
            cv2.line(img, (cx, cy), (cx-300, (cy - int(300*gradient))), (200, 0, 0), 1)
            print("centroid = ("+str(cx)+","+str(cy)+")")
            print("principle angle: "+str(pa))
    return img, cxs, cys, pas

def move(x, y, z, a, grip=-1):
    target = "%f, %f, %f, -180.00, 0.0, %f" % (x, y, z, a)
    script = "PTP(\"CPP\","+target+",100,200,0,false)"
    send_script(script)
    if grip >= 0: set_io(grip)
    return

class ImageSub(Node):
    def __init__(self, nodeName):
        super().__init__(nodeName)
        self.subscription = self.create_subscription(Image, 
        'techman_image', self.image_callback, 10)
        self.subscription
    
    def image_callback(self, data):
        self.get_logger().info('Received image')

        # TODO (write your code here)
        bridge = cv_bridge.CvBridge()
        img = bridge.imgmsg_to_cv2(data, data.encoding)
        cv2.imwrite('./output.jpg', img)
        img, cxs, cys, angles = CalcCentroid(img)
        
        tm = [[0.7517, -0.6453, 215.3364], [-0.6939, -0.68, 572.6126], [0, 0, 1]]
        s =  0.3617993849

        oxs = []
        oys = []
        oas = []
        for cx, cy, angle in zip(cxs, cys, angles):
            oxs.append(tm[0][0] * cx * s + tm[0][1] * cy * s + tm[0][2])
            oys.append(tm[1][0] * cx * s + tm[1][1] * cy * s + tm[1][2])
            oas.append(135 + 90 - angle)

        plane_h = 200.0
        move_h = 300.0
        grab_h = 125.0
        release_h = 200.0
        object_h = 25.0

        ra = 90.0
        rx = 300.0
        ry = 300.0

        for ox, oy, oa in zip(oxs, oys, oas):
            move(ox, oy, move_h, oa, 0.0)
            time.sleep(1)
            move(ox, oy, grab_h, oa, 1.0)
            time.sleep(1)
            move(ox, oy, move_h, ra)
            time.sleep(1)
            move(rx, ry, move_h, ra)
            time.sleep(1)
            move(rx, ry, release_h, ra, 0.0)
            time.sleep(1)
            move(rx, ry, move_h, ra)
            time.sleep(1)
            release_h += object_h

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

def main(args=None):

    rclpy.init(args=args)

    #--- move command by joint angle ---#
    # script = 'PTP(\"JPP\",45,0,90,0,90,0,35,200,0,false)'

    #--- move command by end effector's pose (x,y,z,a,b,c) ---#
    # targetP1 = "398.97, -122.27, 748.26, -179.62, 0.25, 90.12"s

    # Initial camera position for taking image (Please do not change the values)
    # For right arm: targetP1 = "230.00, 230, 730, -180.00, 0.0, 135.00"
    # For left  arm: targetP1 = "350.00, 350, 730, -180.00, 0.0, 135.00"
    targetP1 = "230.00, 230, 750, -180.00, 0.0, 135.00"
    targetP2 = "300.00, 100, 500, -180.00, 0.0, 135.00"
    script1 = "PTP(\"CPP\","+targetP1+",100,200,0,false)"
    script2 = "PTP(\"CPP\","+targetP2+",100,200,0,false)"

    

    send_script(script1)

    send_script("Vision_DoJob(job1)")
    cv2.waitKey(1)

    node = ImageSub('image_sub')
    rclpy.spin(node)
    
    #send_script(script2)

# What does Vision_DoJob do? Try to use it...
# -------------------------------------------------

    #send_script("Vision_DoJob(job1)")
    #cv2.waitKey(1)
#--------------------------------------------------
    
    set_io(0.0)# 1.0: close gripper, 0.0: open gripper
    #set_io(0.0)

    #rclpy.shutdown()

if __name__ == '__main__':
    main()
