import cv2
import math
import matplotlib.pyplot as plt

for t in range(4):
    original = cv2.imread("images/er7-"+str(t+1)+".jpg")

    img = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (9, 9), 0)
    img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)[1]
    contours, _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    texts = ""
    for c in contours:
        M = cv2.moments(c)
        cx = M["m10"] / M["m00"]
        cy = M["m01"] / M["m00"]
        u20 = M["m20"] / M["m00"] - cx ** 2
        u02 = M["m02"] / M["m00"] - cy ** 2
        u11 = M["m11"] / M["m00"] - cx * cy
        cx = int(cx)
        cy = int(cy)
        pa = 0.5 * math.atan2(2 * u11, u20 - u02)
        gradient = math.tan(pa)
        cv2.circle(original, (cx, cy), 5, (0, 0, 255), -1)
        cv2.line(original, (cx, cy), (cx+300, (cy + int(300*gradient))), (255, 0, 0), 2)
        cv2.line(original, (cx, cy), (cx-300, (cy - int(300*gradient))), (255, 0, 0), 2)
        pa *= 180 / math.pi
        text = "\ncentroid = ("+str(cx)+","+str(cy)+"), principle angle: "+str(pa)
        print(text)
        texts += text
    result = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    plt.imshow(result)
    plt.title(texts, fontsize=10)
    plt.show()
