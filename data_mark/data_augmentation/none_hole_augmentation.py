#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/14 15:12
# @Author  : Wang Zixv
# @Site    : 
# @File    : none_hole_augmentation.py
# @Software: PyCharm
import numpy as np
import pandas as pd
import cv2
import os
import random
import csv


# 获取图片亮度
def check_bright(path):
    rgb_image = cv2.imread(path)
    image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
    return image.mean()


# 生成一次参数调整的值
def gen_avg(img_brightness):
    # 偏移坐标
    move_x = random.randint(1, 25) * -1
    move_y = random.randint(1, 25) * -1

    # 亮度调整
    bright_a = 1.8
    if img_brightness < 80:
        bright_b = random.uniform(1.0, 2)
    else:
        bright_b = random.uniform(0, 1.3)

    # 确定翻转方式
    key = random.randint(1, 12)
    if key < 4:
        flip_key = -1
    elif 4 <= key < 8:
        flip_key = 0
    else:
        flip_key = 1
    return move_x, move_y, bright_a, bright_b, flip_key


# 调整图片，并保存
def img_augmentation(img, move_x, move_y, x, y, bright_a, bright_b, flip_key):
    # 调整新图像的亮度
    img_aug = cv2.convertScaleAbs(img, bright_a, bright_b)
    # 对图像进行翻转
    '''
    0 means flipping around the x-axis
    and positive value (for example, 1) means flipping around y-axis.
    Negative value (for example, -1) means flipping around both axes.
    '''
    img_aug = cv2.flip(img_aug, flip_key)
    # # 计算坐标
    new_x, new_y = calculate_after_flip(x, y, img, flip_key)
    # 对图片进行平移
    rows, cols, channels = img_aug.shape
    M = np.float32([[1, 0, move_x], [0, 1, move_y]])
    # cv.warpAffine()第三个参数为输出的图像大小，值得注意的是该参数形式为(width, height)。
    # 将图像进行平移以及切割
    img_aug = cv2.warpAffine(img_aug, M, (cols + move_x, rows + move_y))
    # 计算坐标 x,y, is changed use new
    new_x = new_x + move_x
    new_y = new_y + move_y
    return img_aug, new_x, new_y


#  calculate_after_flip

def calculate_after_flip(x, y, img, flip_key):
    x_ = x
    y_ = y
    rows, cols, channels = img.shape
    # calculate coordinates after flipping
    if flip_key == 0:  # vertical
        y_ = rows - y_
    elif flip_key > 0:  # horizontal
        x_ = cols - x_
    elif flip_key < 0:  # vertical & horizontal
        x_ = cols - x_
        y_ = rows - y_
    return x_, y_


# 生成新的图片信息并写入csv文件
def save_new_img_info(new_img_path_root, img_name, img, new_csv_path, info):
    # save new img
    new_path = os.path.join(new_img_path_root, img_name)
    cv2.imwrite(new_path, img)
    # # save circle info
    # out = open(new_csv_path, 'a', encoding="utf-8-sig", newline='')
    # # 设定写入模式
    # csv_write = csv.writer(out, dialect='excel')
    # csv_write.writerow(info)
    # print("Write img and img_info to file is done!")


# generate new image name
def generate_new_name(img_path, id=0):
    path_list = os.path.split(img_path)
    img_name = path_list[-1]
    new_name = img_name[:-4] + "_" + str(id) + ".jpg"
    return new_name


# 获取包含图片的文件夹路径
def get_file_contents(dir_name, pathList):
    for root, dirs, files in os.walk(dir_name):
        # 遍历文件
        for file in files:
            path = os.path.join(root, file)
            pathList.append(path)

    return pathList


if __name__ == '__main__':
    raw_data = "C:\\Users\\Admin\\Desktop\\none_hole"

    generate_img_dir_path = "E:\\progectlocation\\01.algorithm\\" \
               "python_tool\\data_mark\\data_augmentation\\" \
               "new_img\\2"
    path_list = []
    # 获取所有图片路径
    path_list = get_file_contents(raw_data, path_list)
    print(path_list)
    x = 0
    y = 0
    # 进行图像调整
    for path in path_list:
        for i in range(15):
            new_img_name = generate_new_name(path, i)
            # 获取亮度
            img_brightness = check_bright(path)
            # 生成调整参数
            move_x, move_y, bright_a, bright_b, flip_key = gen_avg(img_brightness)
            img = cv2.imread(path)
            # 进行图片处理
            img_aug, new_x, new_y = img_augmentation(img, move_x, move_y, \
                                                     x, y, bright_a, bright_b, flip_key)
            if img_aug.mean() < 60:
                i -= 1
                continue
            # 保存新图片
            save_new_img_info(generate_img_dir_path, new_img_name, img_aug,\
                              new_csv_path=None, info=None)