import cv2
import math
import matplotlib.pyplot as plt

for t in range(4):
    img = cv2.imread("er7-"+str(t+1)+".jpg")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (9, 9), 0)
    img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)[1]
    contours, _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        M = cv2.moments(c)
        cX = M["m10"] / M["m00"]
        cY = M["m01"] / M["m00"]
        u20 = M["m20"] / M["m00"] - cX ** 2
        u02 = M["m02"] / M["m00"] - cY ** 2
        u11 = M["m11"] / M["m00"] - cX * cY
        cX = int(cX)
        cY = int(cY)
        pa= 0.5 * math.atan2(2 * u11, u20 - u02)
        gradient=math.tan(pa)
        cv2.circle(img, (cX, cY), 7, (0, 0, 255), -1)
        cv2.line(img, (cX, cY), (cX+300, (cY + int(300*gradient))), (200, 0, 0), 1)
        cv2.line(img, (cX, cY), (cX-300, (cY - int(300*gradient))), (200, 0, 0), 1)
        pa *= 180 / math.pi
        print("centroid = ("+str(cX)+","+str(cY)+")")
        print("principle angle: "+str(pa))
    result = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(result)
    plt.show()
