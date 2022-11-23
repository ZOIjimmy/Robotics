import cv2
import numpy as np
import os
import glob

mtx = np.array(
    [[2.65638724e+03, 0.00000000e+00, 7.07835421e+02],
     [0.00000000e+00, 2.65231835e+03, 4.13485582e+02],
     [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

dist = np.array([[-5.39169704e-01, 2.68456414e+01,
                  6.10568726e-03, 7.99300217e-03, -3.45321357e+02]])

rvecs = np.array([
    [[-0.0156484], [0.02297492], [1.17669228]],
    [[-0.04530588], [0.0285935], [0.4085406]],
    [[-0.01357472], [-0.00160925], [-0.03894093]],
    [[-0.01395321], [-0.00513307], [-0.09189605]],
    [[-0.01256387], [-0.03150466], [0.37326597]],
    [[-0.00760046], [-0.00351973], [-1.28859561]],
    [[-0.04886651], [0.0038072], [0.43286323]],
    [[0.05934489], [-0.25505039], [-0.48311125]],
    [[0.02831089], [0.04348857], [1.24757135]],
    [[-0.04936149], [0.02539492], [0.99237457]]])

tvecs = np.array([
    [[4.84412468], [1.6542452], [54.8366371]],
    [[5.33773011e-02], [-2.88550399e+00], [5.52271690e+01]],
    [[-10.70823692], [-4.35786753], [55.09865108]],
    [[-8.97989256], [1.97461715], [54.92068258]],
    [[-5.89632849], [-5.2737655], [55.03205856]],
    [[1.45182512], [6.58386009], [54.69241777]],
    [[-3.08258252], [-0.29383626], [55.1114095]],
    [[-14.08119309], [-2.88373906], [53.99016936]],
    [[6.53025321], [-3.91689003], [54.78554231]],
    [[1.14725789], [-1.961374], [55.21853946]]])


def Calibrate(img):
    h, w = img.shape[:2]
    print(h, w)
    img = cv2.resize(img, (int(w*1), int(h*1)))
    if h > w:
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    h, w = img.shape[:2]
    print(cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h)))
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(
        mtx, dist, (w, h), 1, (w, h))
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    x, y, w, h = roi
    print(x, y, h, w)
    dst = dst[y:y+h, x:x+w]

    cv2.imshow("undistorted img", dst)
    cv2.waitKey(0)
    cv2.imwrite('./output/calibresult.jpg', dst)
    return dst

# criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# objp = np.zeros((6*8, 3), np.float32)
# objp[:,:2] = np.mgrid[0:6, 0:8].T.reshape(-1, 2)

# objpoints = []
# imgpoints = []

# images = glob.glob('./output/*.jpg')
# for fname in images:
#     img = cv2.imread(fname)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     ret, corners = cv2.findChessboardCorners(gray, (6, 8), cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

#     if ret == True:
#         objpoints.append(objp)
#         corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

#         imgpoints.append(corners2)

#         img = cv2.drawChessboardCorners(img, (6, 8), corners2, ret)
#         # cv2.imshow("checkerboard img", img)
#         # cv2.waitKey(0)

# ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None,    None)

# print("Camera matrix : ", mtx)
# print(type(mtx))
# print("dist : ", dist)
# print("rvecs : ", rvecs)
# print("tvecs : ", tvecs)
# for i in rvecs:
#     print(i)


num = 0
images = glob.glob('./output/o.jpg')
print(images)
img = cv2.imread(images[0])
img = Calibrate(img)
cv2.imshow('hi', img)
cv2.waitKey(0)
# img = Calibrate(images)
# cv2.imshow('jo', img)
