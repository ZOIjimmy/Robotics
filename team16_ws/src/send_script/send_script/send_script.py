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
import numpy as np
# arm client


mtx = np.array(
    [[2.65638724e+03,0.00000000e+00,7.07835421e+02],
    [0.00000000e+00,2.65231835e+03,4.13485582e+02],
    [0.00000000e+00,0.00000000e+00,1.00000000e+00]])

dist = np.array([[-5.39169704e-01, 2.68456414e+01, 6.10568726e-03, 7.99300217e-03, -3.45321357e+02]])

rvecs = np.array([
    [[-0.0156484 ], [ 0.02297492], [ 1.17669228]], 
    [[-0.04530588], [ 0.0285935 ], [ 0.4085406 ]], 
    [[-0.01357472], [-0.00160925], [-0.03894093]],
    [[-0.01395321], [-0.00513307], [-0.09189605]], 
    [[-0.01256387], [-0.03150466], [ 0.37326597]],
    [[-0.00760046], [-0.00351973], [-1.28859561]],
    [[-0.04886651], [ 0.0038072 ], [ 0.43286323]],
    [[ 0.05934489], [-0.25505039], [-0.48311125]],
    [[ 0.02831089], [ 0.04348857], [ 1.24757135]],
    [[-0.04936149], [ 0.02539492], [ 0.99237457]] ])

tvecs =  np.array([
    [[ 4.84412468], [ 1.6542452 ], [54.8366371 ]],
    [[ 5.33773011e-02], [-2.88550399e+00], [ 5.52271690e+01]],
    [[-10.70823692], [ -4.35786753], [ 55.09865108]],
    [[-8.97989256], [ 1.97461715], [54.92068258]],
    [[-5.89632849], [-5.2737655 ], [55.03205856]],
    [[ 1.45182512], [ 6.58386009], [54.69241777]],
    [[-3.08258252], [-0.29383626], [55.1114095 ]],
    [[-14.08119309],[ -2.88373906],[ 53.99016936]],
    [[ 6.53025321], [-3.91689003], [54.78554231]],
    [[ 1.14725789], [-1.961374  ], [55.21853946]] ])

##TODO fix
def Calibrate(img):
    h, w = img.shape[:2]
    print(h, w)
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

    cv2.imshow("undistorted img", dst)
    cv2.waitKey(0)
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

def _open():
    set_io(0.0)

def _close():
    set_io(1.0)

def move(x, y, z, a, grip=-1):
    target = "%f, %f, %f, -180.00, 0.0, %f" % (x, y, z, a)
    script = "PTP(\"CPP\","+target+",100,200,0,false)"
    send_script(script)
    if grip >= 1: _open()
    elif grip >= 0: _close()
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
    grab_h = 125.0

    ra = 90.0
    rx = 300.0
    ry = 300.0

    move(ox, oy, move_h, oa, 0)
    move(ox, oy, grab_h, oa, 1)
    move(ox, oy, move_h, ra)
    move(rx, ry, move_h, ra)
    move(rx, ry, release_h, ra, 0)
    move(rx, ry, move_h, ra)

class ImageSub(Node):
    def __init__(self, nodeName):
        super().__init__(nodeName)
        self.subscription = self.create_subscription(Image, 
        'techman_image', self.image_callback, 10)
        self.subscription
    
    def image_callback(self, data):
        self.get_logger().info('Received image')

        bridge = cv_bridge.CvBridge()
        img = bridge.imgmsg_to_cv2(data, data.encoding)
        k = cv2.imwrite('./output/'+str(i)+'.jpg', img)
        img = Calibrate(img)
        areas, xs, ys, angles = CalcCentroid(img)
        
        #TODO transformation matrix and scaling
        tm = [[0.7517, -0.6453, 215.3364], [-0.6939, -0.68, 572.6126], [0, 0, 1]]
        s =  0.3617993849

        oxs = []
        oys = []
        oas = []
        for x, y, angle in zip(xs, ys, angles):
            oxs.append(tm[0][0] * x * s + tm[0][1] * y * s + tm[0][2])
            oys.append(tm[1][0] * x * s + tm[1][1] * y * s + tm[1][2])
            oas.append(135 + 90 - angle)
        
        # TODO change to 0 when all done
        release_h = 200.0
        object_h = 25.0

        # TODO get object size
        # cube_min = 
        # cube_max = 
        # pot_min = 
        # pot_max = 

        for a, ox, oy, oa in zip(areas, oxs, oys, oas):
            # if a > cube_min and a < cube_max:
                StackCube(ox, oy, oa, release_h)
                release_h += object_h
            # elif a > pot_min and a > pot_min:
                # PourPot(ox, oy, oa)

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
    targetP1 = "230.00, 230, 730, -180.00, 0.0, 135.00"
    targetP2 = "230.00, 230, 700, -180.00, 0.0, 135.00"

    script = "PTP(\"CPP\","+targetP2+",100,200,0,false)"
    send_script(script)
    set_io(0.0)# 1.0: close gripper, 0.0: open gripper

# What does Vision_DoJob do? Try to use it...
# -------------------------------------------------
    send_script("Vision_DoJob(job1)")
    cv2.waitKey(1)
#--------------------------------------------------
    node = ImageSub('image_sub')
    rclpy.spin(node)
    
    script = "PTP(\"CPP\","+targetP1+",100,200,0,false)"
    send_script(script)
    set_io(0.0)# 1.0: close gripper, 0.0: open gripper

    #rclpy.shutdown()

if __name__ == '__main__':
    main()
