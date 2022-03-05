#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/24 13:33
# @Author  : Wang Zixv
# @Site    : 
# @File    : draw_circle.py.py
# @Software: PyCharm
import os
import sys

import cv2

# todo 遍历文件夹下所有的图片以及图片的文件夹目录
def get_file_contents_2(dir_name, _path_list, target_type):
    for root, dirs, files in os.walk(dir_name):
        # 遍历文件

        for img_file in files:
            img_path = os.path.join(root, img_file)
            if img_path.endswith(target_type):
                _path_list.append(img_path)

    return _path_list


def draw_circle(img_path_list, result_path, radius_coefficient=0.7):
    for img_path in img_path_list:
        img_name = img_path.split("\\")[-1]
        img = cv2.imread(img_path)
        # 绘制的圆的参数 高，宽，位数
        c_x, c_y, c_r = int(img.shape[1] / 2), int(img.shape[0] / 2), int(
            ((int(img.shape[1] / 2) + int(img.shape[0] / 2)) / 2 * radius_coefficient))
        cv2.circle(img, (c_x, c_y), c_r, (0, 0, 0), -1)
        path = os.path.join(result_path, img_name)
        print(img.shape)
        print(c_x, c_y, c_r)
        print(path)
        cv2.imwrite(path, img)


if __name__ == '__main__':
    # 图片路径
    # ori_path = sys.argv[1]
    ori_path = "E:\\02.PhotoData\\Jidong\\Data\\Production_sampling\\20220216\\station2\\station_2_split\\huajian_img"
    # 生成的绘制完成圆的路径
    result_path = ori_path + "_circle"
    if not os.path.exists(result_path):
        os.mkdir(result_path)
    ori_img_path_list = []
    ori_img_path_list = get_file_contents_2(ori_path, ori_img_path_list, "jpg")
    print(ori_img_path_list)

    draw_circle(ori_img_path_list, result_path)
