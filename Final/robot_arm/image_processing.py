import cv2
import math

def CalcCentroid(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (9, 9), 0)
    img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)[1]
    contours, _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    areas, xs, ys, pas = [], [], [], []
    for c in contours:
        area = cv2.contourArea(c)
        areas.append(area)
        (x, y), (width, height), pa = cv2.minAreaRect(c)
        if width <= height:
            pa += 90
        angle = pa * math.pi / 180

        xs.append(x)
        ys.append(y)
        pas.append(pa)
    return areas, xs, ys, pas


def uv2xyTrans(u, v):
    tm = [[0.3410, -0.3493, 234.4492], [-0.3453, -0.3514, 687.1838], [0, 0, 1]]
    # tm = [[0.34475, -0.3539, 253.5828], [-0.3455, -0.35017, 687.6978], [0, 0, 1]]
    x = tm[0][0] * u + tm[0][1] * v + tm[0][2]
    y = tm[1][0] * u + tm[1][1] * v + tm[1][2]
    return (x, y)