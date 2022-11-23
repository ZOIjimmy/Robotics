#!/usr/bin/env python
from ast import Num
import rclpy

from rclpy.node import Node

import sys
sys.path.append('/home/robot/colcon_ws/install/tm_msgs/lib/python3.6/site-packages')
from tm_msgs.msg import *
from tm_msgs.srv import *

from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
import numpy as np
import matplotlib.pyplot as plt

class ImageSub(Node):
    def __init__(self, nodeName):
        super().__init__(nodeName)
        self.subscription = self.create_subscription(Image, 
        'techman_image', self.image_callback, 10)
        self.subscription
        self.num=0
    
    def image_callback(self, data):
        self.get_logger().info('Received image')
        # print(data.shape)
        # img = CvBridge.imgmsg_to_cv2(data.data,'bgr8')
        img = np.array(data.data)
        img = img.reshape((data.height,data.width,3))
        print(img.shape)
        gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray,(3,3),0)
        ret, thresh = cv2.threshold(blur,220,255,cv2.THRESH_BINARY)
        img_, contours, hierarchy= cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        # print(contours)
        # print(cv2.__version__)
        # for (i,c) in enumerate(contours):
        #     # print(c.shape)
        #     if cv2.contourArea(c) >600:
        #         M=cv2.moments(c)
        #         cx = M['m10']/M['m00']
        #         cy = M['m01']/M['m00']
        #         phi = 0.5*np.arctan2(2*M['mu11'],M['mu20']-M['mu02'])
        #         ## 90 deg to 135 deg
        #         print(cx,cy,phi)
        #         # if phi > 0 :
        #         if cy-cx*np.tan(phi) >= 0:
        #             start_point = (0,int(cy-cx*np.tan(phi)))
        #         else:
        #             start_point = (int(cx-cy/np.tan(phi)),0)
        #         rows, cols = img.shape[:2]
        #         if cy+(cols-cx)*np.tan(phi) <= rows :
        #             end_point = (cols,int(cy+(cols-cx)*np.tan(phi)))
        #         else:
        #             end_point = (int(cx+(rows-cy)/np.tan(phi)),rows)
        #         work_img = img.copy()
        #         work_img = cv2.line(work_img,start_point,end_point,(0,0,255),1)
        #         work_img = cv2.circle(work_img,(int(cx),int(cy)),3,(255,0,0),-1)
        #         fig = plt.figure()
        #         plt.imshow(work_img)
        #         plt.ylabel('y')
        #         plt.xlabel('Centroid = (%f,%f)\n Principle angle = %f degree'%(cx,cy,phi*180/np.pi))
        #         fig.savefig("%d.png"%i)
        cv2.imwrite('%d.jpg'%self.num,img)
        # print('save num:',self.num)
        self.num += 1 
        # cv2.waitKey(1)
        # TODO (write your code here)

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