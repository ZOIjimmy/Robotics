#!/usr/bin/env python
import rclpy

from rclpy.node import Node

import sys
sys.path.append('/home/robot/colcon_ws/install/tm_msgs/lib/python3.6/site-packages')
from tm_msgs.msg import *
from tm_msgs.srv import *

from sensor_msgs.msg import Image
import cv_bridge

def CalcCentroid(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (9, 9), 0)
    img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)[1]
    contours, _, _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cxs, cys, pas = [], [], []
    for c in contours:
        M = cv2.moments(c)
        if M["00"] >= 1000:
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

def grab(x, y, z, a, grip=-1):
    target = "%f, %f, %f, -180.00, 0.0, %f" % (x, y, z, a)
    script = "PTP(\"CPP\","+target+",100,200,0,false)"
    send_script(script)
    if grab >= 0: set_io(grip)
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
        img, cxs, cys, angles = CalcCentroid(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        msg = ""
        for cx, cy, angle in zip(cxs, cys, angles):
            msg += "Centroid:(" + str(cx) + "," + str(cy)+")\nPrinciple angle:" + str(angle) + "\n"
        plt.imshow(img)
        plt.draw()
        text = plt.figtext(0.5, 0.01, output_msg ,va="baseline", ha="center", fontsize=10)
        plt.show(block=False)
        
        tm = [[0.7517, -0.6453, 215.3364], [-0.6939, -0.68, 572.6126], [0, 0, 1]]
        s =  0.3617993849

        oxs = []
        oys = []
        oas = []
        for cx, cy, angle in zip(cxs, cys, angles):
            oxs.append(tm[0][0] * cx * s + tm[0][1] * cy * s + tm[0][2])
            oys.append(tm[1][0] * cx * s + tm[1][1] * cy * s + tm[1][2])
            oas.append(135 + 90 - angle)

        plane_h = 100.0
        move_h = 200.0
        grab_h = 100.0
        release_h = 100.0
        object_h = 25.0

        ra = 90.0
        rx = 300.0
        ry = 300.0

        for ox, oy, oa in zip(oxs, oys, oas):
            move(ox, oy, move_h, oa)
            time.sleep(1)
            move(ox, oy, grab_h, oa, 1)
            time.sleep(1)
            move(ox, oy, move_h, ra)
            time.sleep(1)
            move(rx, ry, move_h, ra)
            time.sleep(1)
            move(rx, ry, release_h, ra, 0)
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

def set_io(state):
    gripper_node = rclpy.create_node('gripper')
    gripper_cli = gripper_node.create_client(SetIO, 'set_io')

    while not gripper_cli.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('service not availabe, waiting again...')
    
    io_cmd = SetIO.Request()
    io_cmd.module = 1
    io_cmd.type = 1
    io_cmd.pin = 0
    io_cmd.state = state
    gripper_cli.call_async(io_cmd)
    gripper_node.destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = ImageSub('image_sub')
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
