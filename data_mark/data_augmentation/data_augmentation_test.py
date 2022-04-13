#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/13 11:50
# @Author  : Wang Zixv
# @Site    : 
# @File    : data_augmentation_test.py
# @Software: PyCharm
'''
参考：https://towardsdatascience.com/top-python-libraries-for-image-augmentation-in-computer-vision-2566bed0533e
'''
'''
这个是测试类，主要用来进行最小单元测试
此类主要用来进行数据扩充，扩充逻辑：
平移，改变亮度，翻转
'''
import numpy as np
import cv2
import os

'''
图像的平移裁切
'''


def panning(img_path, move_x, move_y):
    img = cv2.imread(img_path, 1)
    rows, cols, channels = img.shape
    M = np.float32([[1, 0, move_x], [0, 1, move_y]])
    # cv.warpAffine()第三个参数为输出的图像大小，值得注意的是该参数形式为(width, height)。
    # 此时直接对平移后的图片进行切割
    # res = cv2.warpAffine(img, M, (cols + move_x, rows + move_y))
    res = cv2.warpAffine(img, M, (cols, rows))
    flip_step = []
    if move_x > 0 and move_y > 0:
        flip_step.append(-1)
    else:
        if move_x > 0:
            flip_step.append(1)
        if move_y > 0:
            flip_step.append(0)
    print("flip_step")
    print(flip_step)
    # 翻转图品之后切割图片再翻转回来
    for step in flip_step:
        img = cv2.flip(img, step)
        print("fan zhuan")
    print(res)
    res = res[0:cols - move_x, 0:rows - move_y]
    print(res)

    for i in range(len(flip_step)-1,-1,-1):
        res = cv2.flip(res, flip_step[i])
        print("fan zhuan 2")
    # save new img
    # new_path = "new_img\\" + os.path.split(img_path)[-1]
    # cv2.imwrite(new_path, res)

    cv2.imshow('before', img)
    cv2.imshow('after', res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


'''
图像亮度调整
'''


def brightness(path, c, b):
    img = cv2.imread(path, cv2.IMREAD_COLOR)  # 打开文件

    # 通过融合两张图片方式实现亮度调整
    rows, cols, chunnel = img.shape
    blank = np.zeros([rows, cols, chunnel], img.dtype)
    dst = cv2.addWeighted(img, c, blank, 1 - c, b)
    cv2.imwrite('./new_img/addWeighted.jpg', dst)

    # 通过cv2.cvtColor把图像从BGR转换到HSV
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # # H空间中，绿色比黄色的值高一点，所以给每个像素+15，黄色的树叶就会变绿
    # turn_green_hsv = img_hsv.copy()
    # turn_green_hsv[:, :, 0] = (turn_green_hsv[:, :, 0] + 15) % 180
    # turn_green_img = cv2.cvtColor(turn_green_hsv, cv2.COLOR_HSV2BGR)
    # cv2.imwrite('./new_img/turn_green.jpg', turn_green_img)
    #
    # # 减小饱和度会让图像损失鲜艳，变得更灰
    # colorless_hsv = img_hsv.copy()
    # colorless_hsv[:, :, 1] = 0.5 * colorless_hsv[:, :, 1]
    # colorless_img = cv2.cvtColor(colorless_hsv, cv2.COLOR_HSV2BGR)
    # cv2.imwrite('./new_img/colorless.jpg', colorless_img)

    # 亮度调整
    darker_hsv = img_hsv.copy()
    darker_hsv[:, :, 2] = 2 * darker_hsv[:, :, 2]
    darker_img = cv2.cvtColor(darker_hsv, cv2.COLOR_HSV2BGR)
    cv2.imwrite('./new_img/darker2.jpg', darker_img)

def brightness2(path, alpha, beta):
    img = cv2.imread(path)
    print(img)
    img_bright = cv2.convertScaleAbs(img, alpha, beta)
    print(img_bright)

    cv2.imshow("img", img)
    cv2.imshow("img_bright", img_bright)
    cv2.imwrite('./new_img/img_bright.jpg', img_bright)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

'''获取图片亮度'''
def get_img_bright(path):
    # TODO 经过测试阈值80就可以
    # 读取图片
    rgb_image = cv2.imread(path)
    image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
    print(path)
    print("图片亮度值为：", image.mean())

'''
图像翻转
'''


def img_flipping(path):
    # >0 	水平翻转
    # =0	垂直翻转
    # <0	水平和垂直翻转
    img = cv2.imread(path)
    f_img_1 = cv2.flip(img,1)
    f_img_0 = cv2.flip(img,0)
    f_img_2 = cv2.flip(img,-1)
    cv2.imshow("img", img)
    cv2.imshow("水平翻转", f_img_1)
    cv2.imshow("垂直翻转", f_img_0)
    cv2.imshow("水平+垂直", f_img_2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    img_path = "testData\\1\\10.jpg"
    img_path2 = "testData\\1\\0.jpg"
    img_path3 = "E:\\PythonProject\\01.factory_photo_data\\"\
                "\\02.training-data\\large_hole_training_data\\"\
                "data_augmentation\\1\\103_8.jpg"
    move_x = 10
    move_y = 10
    # img_path = "new_img/darker.jpg"
    # panning(img_path, move_x, move_y)
    # brightness(img_path, c=5, b=20)

    # alpha = 1.5
    # beta = 2
    # brightness2(img_path, alpha, beta)
    # get_img_bright(img_path)
    # get_img_bright(img_path2)
    # img_flipping(img_path)
    img = cv2.imread(img_path3)
    print(img.mean())