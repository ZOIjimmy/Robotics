import cv2
import numpy as np
import os
import glob

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((6*8, 3), np.float32)
objp[:,:2] = np.mgrid[0:6, 0:8].T.reshape(-1, 2)

objpoints = []
imgpoints = [] 

images = glob.glob('./Assignment3/PartA/Camera_Calib/final_checkonly/*.jpg')
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (6, 8), cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    
    if ret == True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        
        imgpoints.append(corners2)

        img = cv2.drawChessboardCorners(img, (6, 8), corners2, ret)    
        cv2.imshow("checkerboard img", img)
        cv2.waitKey(0)

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("Camera matrix : ", mtx)
print("dist : ", dist)
print("rvecs : ", rvecs)
print("tvecs : ", tvecs)

num = 0
images = glob.glob('./Assignment3/PartA/Camera_Calib/final_cap/*.jpg')
for fname in images:    
    num += 1
    img = cv2.imread(fname)
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    cv2.imshow("undistorted img", dst)
    cv2.waitKey(0)
    cv2.imwrite('./Assignment3/PartA/Camera_Calib/result/calibresult_{}.jpg'.format(num), dst)

mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    mean_error += error
print( "total error: {}".format(mean_error/len(objpoints)) )
