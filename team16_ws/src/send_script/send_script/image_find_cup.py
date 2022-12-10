from rclpy.node import Node
from sensor_msgs.msg import Image
import cv_bridge
import cv2
import numpy as np
   
from .image_processing import uv2xyTrans

class FindCup(Node):
    def __init__(self, nodeName, deltaDis):
        super().__init__(nodeName)
        self.subscription = self.create_subscription(Image, 
        'techman_image', self.image_callback, 10)
        self.subscription
        self.circle_x, self.circle_y, self.circle_r = 0, 0, 0
        self.deltaDis = deltaDis

    def image_callback(self, data):
        self.get_logger().info('Received image')
        self.get_logger().info('Start finding cup')

        bridge = cv_bridge.CvBridge()
        img = bridge.imgmsg_to_cv2(data, data.encoding)
        k = cv2.imwrite('./output/cup/cup.jpg', img)

        # process image
        processImg = img.copy()
        processImg = cv2.cvtColor(processImg, cv2.COLOR_BGR2GRAY) 
        processImg = cv2.GaussianBlur(processImg, (5, 5), 0)

        # detect circle
        circles = cv2.HoughCircles(processImg, cv2.HOUGH_GRADIENT, 1.2, 1000, param2=10, minRadius=100, maxRadius=150)

        if circles is not None:
            # convert coordinate to int
            circles = np.round(circles[0, :]).astype("int")

            for (x, y, r) in circles:
                cv2.circle(processImg, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(processImg, (x-5, y-5), (x + 5, y + 5), (0, 128, 255), -1)
            
        
        k = cv2.imwrite('./output/cup/cup_processed.jpg', processImg)

        print(circles.size)
        if circles.size > 1:
            self.get_logger().info('Caution more the one circle detected')

        cupPos = circles[0]
        print("cupPos", cupPos[0], cupPos[1])
        (cupX, cupY) = uv2xyTrans(cupPos[0], cupPos[1])
        print("cup world", cupX, cupY)


        self.circle_x, self.circle_y = (cupX + self.deltaDis[0], cupY + self.deltaDis[1])
        print("circle x, y:", self.circle_x , "," , self.circle_y)
        # self.circle_r = cupPos[2]