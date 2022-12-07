import cv2
import numpy as np
import math

img = cv2.imread("color/0.jpg")
imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_red = np.array([0, 65, 65])
upper_red = np.array([10, 255, 255])
mask_red = cv2.inRange(imghsv, lower_red, upper_red)
contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
red_dots = []
for c in contours:
    area = cv2.contourArea(c)
    if area <= 100 or area >= 800:
        continue
    (x, y), (width, height), pa = cv2.minAreaRect(c)
    if area/width/height <= 0.6:
        continue
    red_dots.append((x, y))
    cv2.drawContours(img, [c], -1, (255, 180, 255), 1)

lower_blue = np.array([90, 60, 80])
upper_blue = np.array([110, 255, 255])
mask_blue = cv2.inRange(imghsv, lower_blue, upper_blue)
contours, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
blue_dots = []
for c in contours:
    area = cv2.contourArea(c)
    if area <= 100 or area >= 800:
        continue
    (x, y), (width, height), pa = cv2.minAreaRect(c)
    if area/width/height <= 0.6:
        continue
    blue_dots.append((x, y))
    cv2.drawContours(img, [c], -1, (255, 180, 255), 1)

lower_green = np.array([40, 70, 70])
upper_green = np.array([80, 255, 255])
mask_green = cv2.inRange(imghsv, lower_green, upper_green)
contours, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
green_dots = []
for c in contours:
    area = cv2.contourArea(c)
    if area <= 100 or area >= 800:
        continue
    (x, y), (width, height), pa = cv2.minAreaRect(c)
    if area/width/height <= 0.6:
        continue
    green_dots.append((x, y))
    cv2.drawContours(img, [c], -1, (255, 180, 255), 1)

print(blue_dots)
print(red_dots)
print(green_dots)
cv2.imshow('image',img)
cv2.waitKey(0)

