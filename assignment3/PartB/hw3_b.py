import cv2
import math
import os
import matplotlib.pyplot as plt

while True:
    print("enter filepath reletive to current working directory")
    print("current working directory is " + os.getcwd())
    print("example: ./images/er7-1.jpg")
    filepath = input("filepath: ")
    fig = plt.figure()
    fig.suptitle("Image: " + os.path.basename(filepath))
    plt.subplots_adjust(
                    bottom=0,
                    wspace=0,
                    hspace=0.42)

    img = cv2.imread(filepath)
    h, w = img.shape[:2]

    # plot original image
    ax = fig.add_subplot(3, 2, 1)
    plt.imshow(img)
    ax.set_title('Original image')

    ori_img = img.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (9, 9), 0)
    img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)[1]
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # plot image after preprocess
    ax = fig.add_subplot(3, 2, 2)
    plt.imshow(img)
    ax.set_title('After preprocess')

    ax = fig.add_subplot(3, 2, 3)
    ax.set_ylim(0, h)
    ax.set_xlim(0, w)
    ax.invert_yaxis()
    ax.set_aspect('equal', adjustable='box')
    ax.set_title('Contour')

    info_centroid_str = "centroids: " 
    info_angle_str = "principle angles(deg): "
    for c in contours:
        # plot image after preprocess
        ax.plot(c[:, 0, 0], c[:, 0, 1])

        M = cv2.moments(c)
        cX = M["m10"] / M["m00"]
        cY = M["m01"] / M["m00"]
        u20 = M["m20"] / M["m00"] - cX ** 2
        u02 = M["m02"] / M["m00"] - cY ** 2
        u11 = M["m11"] / M["m00"] - cX * cY
        icX = int(cX)
        icY = int(cY)
        pa= 0.5 * math.atan2(2 * u11, u20 - u02)
        slope=math.tan(pa)
        cv2.circle(ori_img, (icX, icY), 7, (0, 0, 255), -1)
        cv2.line(ori_img, (icX, icY), (icX+300, (icY + int(300*slope))), (200, 0, 0), 1)
        cv2.line(ori_img, (icX, icY), (icX-300, (icY - int(300*slope))), (200, 0, 0), 1)
        pa *= 180 / math.pi
        info_centroid_str += "("+str(round(cX, 4))+","+str(round(cY, 4))+"),  "
        info_angle_str += str(round(pa, 4)) + ",  "

    result = cv2.cvtColor(ori_img, cv2.COLOR_BGR2RGB)
    info_centroid_str = info_centroid_str[:-3]
    info_angle_str = info_angle_str[:-3]
    print(info_centroid_str)
    print(info_angle_str)

    # plot result
    ax = fig.add_subplot(3, 2, 4)
    plt.imshow(result)
    ax.set_title('Result')
    plt.figtext(0.5, 0.15, info_centroid_str + "\n" + info_angle_str,
    ha="center", fontsize=10, bbox={"facecolor":"green", "alpha":0.5, "pad":5})
    plt.show(block=False)
    reply = input('continue? (y/n): ').lower().strip()
    if reply[0] == 'n':
        break
