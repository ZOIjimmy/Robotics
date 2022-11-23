#!/usr/bin/env python
import rclpy

from rclpy.node import Node

import sys
sys.path.append('/home/robot/colcon_ws/install/tm_msgs/lib/python3.6/site-packages')
from tm_msgs.msg import *
from tm_msgs.srv import *

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from datetime import datetime
from pathlib import Path
import json


def findCentroid(M):
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    return cx, cy

def drawAndSave(img):
    areaThres = 100

    ori_img = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 127, 255, 0)
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    pos = []
    for i in range(len(contours)):
        cnt = contours[i]
        M = cv2.moments(cnt)
        area = M['m00']
        if area > areaThres:
            # draw the centroid
            cx, cy = findCentroid(M)
            cv2.circle(ori_img,(cx,cy), 2, (255, 0, 0), 6)
            cv2.drawContours(ori_img, [cnt], 0, (0,255,0), 3)
            pos.append((cx, cy))

    return ori_img, pos

class ImageSub(Node):
    def __init__(self, nodeName):
        super().__init__(nodeName)
        self.subscription = self.create_subscription(Image, 
        'techman_image', self.image_callback, 10)
        self.subscription
    
    def image_callback(self, data):
        self.get_logger().info('Received image')
        
        # TODO (write your code here)
        self.bridge = CvBridge()
        cv_image = self.bridge.imgmsg_to_cv2(data)
        cv_image, cent_pos = drawAndSave(cv_image)

        base_dir = '/home/robot/workspace2/team10_ws/src/send_script/send_script/images/'
        file_name = datetime.now()
        cv2.imwrite(base_dir + '{}.png'.format(file_name), cv_image)
        pos_file = Path(base_dir + str(file_name) + '.json')
        pos_file.write_text(json.dumps(cent_pos))
        


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