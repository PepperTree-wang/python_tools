#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/13 15:32
# @Author  : Wang Zixv
# @Site    :
# @File    : data_augmentation.py
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


def get_ratio():
    ratio = random.randint(7, 13) * 0.1
    return ratio


# 获取图片的坐标信息
def get_coordinate(path_root, df, idx):
    # 获取图片路径
    row = df.iloc[idx]
    img_path = os.path.join(str(row['label']), row['img_path'])
    img_path = os.path.join(path_root, img_path)
    # 获取冲孔坐标
    x = row['x']
    y = row['y']
    r = row['r']
    label = row['label']

    return img_path, x, y, r, label


# 生成一次参数调整的值
def gen_avg(img_brightness):
    # 偏移坐标
    move_x = random.randint(1, 25) * -1
    move_y = random.randint(1, 25) * -1

    # 亮度调整
    bright_a = 1.5
    if img_brightness < 80:
        bright_b = random.uniform(1.0, 1.5)
    else:
        bright_b = random.random()

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
def img_augmentation(img,x, y, r):
    # generate parameter
    move_x, move_y, bright_a, bright_b, flip_key = gen_avg(brightness)
    # print(brightness)
    # print(move_x, move_y, bright_a, bright_b, flip_key)

    ratio = get_ratio()
    bool_list = np.random.randint(2, size=4)
    ifcrop, ifbright, ifflip, ifresize = bool_list[0], bool_list[1], bool_list[2], bool_list[3]
    # print(bool_list)

    if ifbright:
        # 调整新图像的亮度
        img_aug = cv2.convertScaleAbs(img, bright_a, bright_b)
    else:
        img_aug = img.copy()
    # 对图像进行翻转
    '''
    0 means flipping around the x-axis
    and positive value (for example, 1) means flipping around y-axis.
    Negative value (for example, -1) means flipping around both axes.
    '''
    if ifflip:
        img_aug = cv2.flip(img_aug, flip_key)
        # # 计算坐标
        new_x, new_y = calculate_after_flip(x, y, img, flip_key)
    else:
        new_x, new_y = x, y

    if ifcrop:
        # 对图片进行平移
        rows, cols, channels = img_aug.shape
        M = np.float32([[1, 0, move_x], [0, 1, move_y]])
        # cv.warpAffine()第三个参数为输出的图像大小，值得注意的是该参数形式为(width, height)。
        # 将图像进行平移以及切割
        img_aug = cv2.warpAffine(img_aug, M, (cols + move_x, rows + move_y))
        # 计算坐标 x,y, is changed use new
        new_x = new_x + move_x
        new_y = new_y + move_y

    new_r = r
    if ifresize:
        img_size = int(img_aug.shape[1] * ratio), int(img_aug.shape[0] * ratio)
        img_aug = cv2.resize(img_aug, img_size, interpolation=cv2.INTER_AREA)

        new_x = int(new_x * ratio)
        new_y = int(new_y * ratio)
        new_r = int(r * ratio)

    return img_aug, new_x, new_y, new_r


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
def save_new_img_info(new_img_path_root, label, img_name, img, new_csv_path, info):
    # save new img
    new_path = new_img_path_root + "\\" + str(label) + "\\" + img_name
    print(new_path)
    cv2.imwrite(new_path, img)
    # save circle info
    out = open(new_csv_path, 'a', encoding="utf-8-sig", newline='')
    # 设定写入模式
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow(info)
    # print("Write img and img_info to file is done!")


# generate new image name
def generate_new_name(img_path, id=0):
    path_list = os.path.split(img_path)
    img_name = path_list[-1]
    new_name = img_name[:-4] + "_" + str(id) + ".jpg"
    return new_name


'''
从已经标记好的csv文件中读取dataframe
之后在csv文件中找到图片的路径
1.对图像进行处理
2.调整圆心坐标
3.保存本条记录
'''
if __name__ == '__main__':
    # raw data info csv file path
    csv_path = ".\\large_1.csv"
    # augmentation data information csv file path
    new_csv_path = "E:\\progectlocation\\01.algorithm\\XingYeAutoParts\\" \
                   "01.training_data\\resize\\resize_data.csv"
    # raw data file path
    path_root = "E:\\progectlocation\\01.algorithm\\XingYeAutoParts\\" \
                "01.training_data\\large_hole_training_data"
    # generated data file path
    new_path_root = "E:\\progectlocation\\01.algorithm\\XingYeAutoParts\\" \
                    "01.training_data\\resize"
    df = pd.read_csv(csv_path)
    # print(len(df))
    # todo range df
    for i in range(len(df)):
        img_path, x, y, r, label = get_coordinate(path_root, df, i)
        # print(img_path, x, y, r)
        brightness = check_bright(img_path)

        for j in range(10):
            new_x = x
            new_y = y
            img = cv2.imread(img_path)
            # generate new image name :1_x.jpg
            img_new_name = generate_new_name(img_path, j)
            # print(img_new_name)

            # generate new img ang new image information
            img_new, new_x_, new_y_, new_r = img_augmentation(img,  new_x, new_y, r)

            # 图像亮度低于25不保存
            if img_new.mean() > 25:
                # print("new img brightness：")
                # print(img_new.mean())
                # save img to file & save info to csv
                info = [img_new_name, new_x_, new_y_, new_r, label]
                # print(info)
                save_new_img_info(new_path_root, label, img_new_name, img_new, new_csv_path, info)
