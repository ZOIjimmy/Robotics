from rclpy.node import Node
from sensor_msgs.msg import Image
import cv_bridge

import cv2
import numpy as np
import os
import glob
import math



def CalibrateFromSource():
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1)

    objp = np.zeros((6*8, 3), np.float32)
    objp[:,:2] = np.mgrid[0:6, 0:8].T.reshape(-1, 2)

    objpoints = []
    imgpoints = []

    images = glob.glob('./output/calibrate_source/*.jpg')
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (6, 8), cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

        if ret == True:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

            imgpoints.append(corners2)

            img = cv2.drawChessboardCorners(img, (6, 8), corners2, ret)
            # cv2.imshow("checkerboard img", img)
            # cv2.waitKey(0)

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    print("mtx:", mtx)
    print("dist:", dist)

    return (ret, mtx, dist, rvecs, tvecs)


##TODO fix
def Calibrate(img):
    (ret, mtx, dist, rvecs, tvecs) = CalibrateFromSource()

    h, w = img.shape[:2]
    print("(w,h):", (w,h))

    #img = cv2.resize(img, (int(w*resizeScale), int(h*resizeScale)))
    if h > w:
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    h, w = img.shape[:2]
    print(cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h)))
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    x, y, w, h = roi
    print(x, y, h, w)
    dst = dst[y:y+h, x:x+w]

    # cv2.imshow("undistorted img", dst)
    # cv2.waitKey(0)
    cv2.imwrite('./output/calibresult.jpg', dst)
    return dst

def CalcCentroid(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (9, 9), 0)
    img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)[1]
    _, contours, _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    areas, xs, ys, pas = [], [], [], []
    for c in contours:
        area = cv2.contourArea(c)
        areas.append(area)
        print("area=", area)
        (x, y), (width, height), pa = cv2.minAreaRect(c)
        if width <= height:
            pa += 90
        angle = pa * math.pi / 180

        # TODO this can maybe detect the teapot by rotating 180 degree
        '''
        mx, my = np.where(img >= 200)
        cx = np.average(mx)
        cy = np.average(my)
        if (cy - y) / (cx - x) / math.tan(pa) < 0:
            pa += 180
        '''

        xs.append(x)
        ys.append(y)
        pas.append(pa)
    return areas, xs, ys, pas

class ImageSub(Node):
    def __init__(self, nodeName):
        super().__init__(nodeName)
        self.subscription = self.create_subscription(Image, 
        'techman_image', self.image_callback, 10)
        self.subscription
        self.oxs = []
        self.oys = []
        self.oas = []

    
    def image_callback(self, data):
        self.get_logger().info('Received image')

        bridge = cv_bridge.CvBridge()
        print("bridge",bridge)
        img = bridge.imgmsg_to_cv2(data, data.encoding)
        k = cv2.imwrite('./output/calibrated.jpg', img)

        # img = Calibrate(img)
        areas, xs, ys, angles = CalcCentroid(img)
        
        # #TODO transformation matrix and scaling
        # tm = [[0.7517, -0.6453, 215.3364], [-0.6939, -0.68, 572.6126], [0, 0, 1]]
        tm = [[0.3410, -0.3493, 234.4492], [-0.3453, -0.3514, 687.1838], [0, 0, 1]]
        # s =  0.361799
        s =  1

        oxs = []
        oys = []
        oas = []
        for x, y, angle in zip(xs, ys, angles):
            oxs.append(tm[0][0] * x * s + tm[0][1] * y * s + tm[0][2])
            oys.append(tm[1][0] * x * s + tm[1][1] * y * s + tm[1][2])
            oas.append(135 + 90 - angle)
        
        print("oxs:", oxs)
        print("oys:", oys)
        print("oas:", oas)
        self.oxs = oxs
        self.oys = oys
        self.oas = oas
        # # TODO change to 0 when all done
        # release_h = 200.0
        # object_h = 25.0

        # # TODO get object size
        # # cube_min = 
        # # cube_max = 
        # # pot_min = 
        # # pot_max = 

        # for a, ox, oy, oa in zip(areas, oxs, oys, oas):
        #     # if a > cube_min and a < cube_max:
        #         StackCube(ox, oy, oa, release_h)
        #         release_h += object_h
        #     # elif a > pot_min and a > pot_min:
        #         # PourPot(ox, oy, oa)