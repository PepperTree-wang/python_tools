import os.path

import cv2
import numpy as np

def main():
    fold = "E:\\TEMP\\haixin\\20220224"
    images = os.listdir(fold)
    i = 0
    for image in images:
        img = cv2.imread(os.path.join(fold, image), 0)
        img = cv2.GaussianBlur(img, (5, 5), 2  )  # 高斯 滤波
        #
        # # 二值化处理，低于阈值的像素点灰度值置为0；高于阈值的值置为参数3
        # ret, thresh1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        # cv2.imshow('BINARY', thresh1)
        #
        # cv2.waitKey(0)
        # # 大于阈值的像素点灰度值置为0；小于阈值置为参数3
        # ret, thresh2 = cv2.threshold(img, 127, 200, cv2.THRESH_BINARY_INV)
        # cv2.imshow('BINARY_INV', thresh2)
        #
        # cv2.waitKey(0)
        # # 小于阈值的像素点灰度值不变，大于阈值的像素点置为该阈值
        # ret, thresh3 = cv2.threshold(img, 127, 255, cv2.THRESH_TRUNC)
        # cv2.imshow('TRUNC', thresh3)
        #
        # cv2.waitKey(0)
        # # 小于阈值的像素点灰度值不变，大于阈值的像素点置为0,其中参数3任取
        # ret, thresh4 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)
        # cv2.imshow('BINARY_TOZERO', thresh4)
        #
        # cv2.waitKey(0)
        # # 大于阈值的像素点灰度值不变，小于阈值的像素点置为0,其中参数3任取
        # ret, thresh5 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO_INV)
        # cv2.imshow('BINARY_TOZERO_INV', thresh5)
        # cv2.waitKey(0)

        ret, thresh1 = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
        im_array = np.array(img)
        grad0, grad1 = np.gradient(im_array)
        grad0 = abs(grad0).astype("uint8")
        grad0[grad0>0] = 255
        cv2.imshow("grad", grad0)
        cv2.waitKey(0)

        rows, cols = grad0.shape
        row = rows - 1
        while row != 0:
            cal = grad0[row-1:row, 0:cols]
            idx = np.argwhere(cal > 0)
            # 白点大于7%，不合格
            if len(idx)>cols*5*0.07:
                break
            row -= 1
        cv2.line(im_array, (0, row), (cols-1, row), (255, 255, 255), 1)

        # 主要API
        # num_labels, labels, stats, centers = cv2.connectedComponentsWithStats(grad0, connectivity=4, ltype=cv2.CV_32S)
        #
        # for t in range(1, num_labels, 1):
        #     x, y, w, h, area = stats[t]
        #     cx, cy = centers[t]
        #
        #     # 绘制图像
        #     cv2.rectangle(grad0, (x, y), (x + w, y + h), 0, 1, 8, 0)
        # erode_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))  # 腐蚀内核
        # grad0 = cv2.erode(grad0, erode_kernel, iterations=1)
        #
        # # 主要API
        # num_labels, labels, stats, centers = cv2.connectedComponentsWithStats(grad0, connectivity=4, ltype=cv2.CV_32S)
        #
        # for t in range(1, num_labels, 1):
        #     x, y, w, h, area = stats[t]
        #     cx, cy = centers[t]
        #
        #     # 绘制图像
        #     cv2.rectangle(grad0, (x, y), (x + w, y + h), 0, 1, 8, 0)
        #
        # erode_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))  # 腐蚀内核
        # grad0 = cv2.erode(grad0, erode_kernel, iterations=1)
        #
        # # 轮廓本身，还有一个是每条轮廓对应的属性。
        # contours, hierarchy = cv2.findContours(grad0.copy(), cv2.RETR_EXTERNAL,
        #                                        cv2.CHAIN_APPROX_SIMPLE)
        #
        # for c in contours:
        #     # compute the rotated bounding box of the contour
        #     box = cv2.minAreaRect(c)
        #     box = cv2.boxPoints(box)
        #     box = np.array(box, dtype="int")
        #     # print("box:", box)
        #     """
        #     draw box on rgb image
        #      box:[[1358 1600]
        #      [1358 1465]
        #      [1462 1465]
        #      [1462 1600]]
        #     """
        #     cv2.line(im_array, (box[0, 0], box[0, 1]), (box[1, 0], box[1, 1]), (0, 255, 0), 1)
        #     cv2.line(im_array, (box[1, 0], box[1, 1]), (box[2, 0], box[2, 1]), (0, 255, 0), 1)
        #     cv2.line(im_array, (box[2, 0], box[2, 1]), (box[3, 0], box[3, 1]), (0, 255, 0), 1)
        #     cv2.line(im_array, (box[3, 0], box[3, 1]), (box[0, 0], box[0, 1]), (0, 255, 0), 1)
        #
        # # lines = cv2.HoughLinesP(grad0, rho=1.1, theta=np.pi / 2, threshold=100,
        # #                         minLineLength=50,  maxLineGap=10)
        # # for line in lines:
        # #     print(line)
        # #     line = line[0]
        # #     cv2.line(grad0, (line[0], line[1]), (line[2], line[3]), color=255, thickness=1)
        # cv2.imshow("grad0", grad0 )
        # cv2.waitKey(0)
        # cv2.imwrite("testData/tidu/" + str(i) + ".jpg", im_array)
        # i = i + 1
        # cv2.imshow("grad0", grad0 )
        cv2.imshow("image", im_array )
        # cv2.imshow("grad1", grad1)
        cv2.waitKey(0)



if __name__ == "__main__":
    main()