from rclpy.node import Node
from sensor_msgs.msg import Image
import cv_bridge

import cv2
import numpy as np
import os
import glob
import math

tm = [[0.3410, -0.3493, 234.4492], [-0.3453, -0.3514, 687.1838], [0, 0, 1]]
# tm = [[0.34475, -0.3539, 253.5828], [-0.3455, -0.35017, 687.6978], [0, 0, 1]]


def CalcCentroid(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (9, 9), 0)
    img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)[1]
    contours, _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    areas, xs, ys, pas = [], [], [], []
    for c in contours:
        area = cv2.contourArea(c)
        areas.append(area)
        print("area=", area)
        (x, y), (width, height), pa = cv2.minAreaRect(c)
        if width <= height:
            pa += 90
        angle = pa * math.pi / 180

        xs.append(x)
        ys.append(y)
        pas.append(pa)
    return areas, xs, ys, pas

def FindColorDots(img):
    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([90, 60, 80])
    upper_blue = np.array([110, 255, 255])
    mask_blue = cv2.inRange(imghsv, lower_blue, upper_blue)
    contours, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blue_dots = []
    for c in contours:
        area = cv2.contourArea(c)
        # print("brue dot area",area)
        if area <= 50 or area >= 800:
            continue
        (x, y), (width, height), pa = cv2.minAreaRect(c)
        newx = tm[0][0] * x + tm[0][1] * y + tm[0][2]
        newy = tm[1][0] * x + tm[1][1] * y + tm[1][2]
        x = (newx-285)*0.9125 + 285
        y = (newy-285)*0.9125 + 285
        blue_dots.append((x, y))
        
    lower_red = np.array([0, 60, 60])
    upper_red = np.array([10, 255, 255])
    mask_red = cv2.inRange(imghsv, lower_red, upper_red)
    contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    red_dots = []
    for c in contours:
        area = cv2.contourArea(c)
        # print("red dot area",area)
        if area <= 50 or area >= 800:
            continue
        (x, y), (width, height), pa = cv2.minAreaRect(c)
        newx = tm[0][0] * x + tm[0][1] * y + tm[0][2]
        newy = tm[1][0] * x + tm[1][1] * y + tm[1][2]
        x = (newx-285)*0.9125 + 285
        y = (newy-285)*0.9125 + 285
        red_dots.append((x, y))

    lower_green = np.array([40, 60, 60])
    upper_green = np.array([55, 255, 255])
    mask_green = cv2.inRange(imghsv, lower_green, upper_green)
    contours, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    green_dots = []
    for c in contours:
        area = cv2.contourArea(c)
        
        if area <= 50 or area >= 800:
            continue
        print("green dot area",area)
        (x, y), (width, height), pa = cv2.minAreaRect(c)
        newx = tm[0][0] * x + tm[0][1] * y + tm[0][2]
        newy = tm[1][0] * x + tm[1][1] * y + tm[1][2]
        x = (newx-285)*0.9125 + 285
        y = (newy-285)*0.9125 + 285
        green_dots.append((x, y))

    return blue_dots, red_dots, green_dots
        
class ImageSub(Node):
    def __init__(self, nodeName):
        super().__init__(nodeName)
        self.subscription = self.create_subscription(Image, 
        'techman_image', self.image_callback, 10)
        self.subscription
        self.areas, self.oxs, self.oys, self.oas = [], [], [], []
        self.blue, self.red, self.green = [], [], []

    def image_callback(self, data):
        self.get_logger().info('Received image')

        bridge = cv_bridge.CvBridge()
        img = bridge.imgmsg_to_cv2(data, data.encoding)

        k = cv2.imwrite('./output/color/1211_01.jpg', img)

        areas, xs, ys, angles = CalcCentroid(img)
        
        tm = [[0.3410, -0.3493, 234.4492], [-0.3453, -0.3514, 687.1838], [0, 0, 1]]
        # tm = [[0.34475, -0.3539, 253.5828], [-0.3455, -0.35017, 687.6978], [0, 0, 1]]

        oxs, oys, oas = [], [], []
        for x, y, angle in zip(xs, ys, angles):
            oxs.append(tm[0][0] * x + tm[0][1] * y + tm[0][2])
            oys.append(tm[1][0] * x + tm[1][1] * y + tm[1][2])
            oas.append(135 + 90 - angle)
        self.areas, self.oxs, self.oys, self.oas = areas, oxs, oys, oas

        self.blue, self.red, self.green = FindColorDots(img)