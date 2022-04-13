#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/28 15:28
# @Author  : Wang Zixv
# @Site    : Qingdao
# @File    : get_img_marked_txt.py
# @Software: PyCharm
# 程序为通过图片名称寻找对应的yolo已经标记的txt文件

import os
import sys
import cv2
import shutil


def get_txt(img_path, txt_path, target_path):
    imgs_name = os.listdir(img_path)
    txt_name_ori = os.listdir(txt_path)
    txt_name = []
    for n in txt_name_ori:
        txt_name.append(n[:-4])

    print(imgs_name)
    for i, name in enumerate(imgs_name):
        print(str(i))
        img_name = imgs_name[i][:-4]
        if img_name in txt_name:
            name = img_name + ".txt"
            print(name)
            source = os.path.join(txt_path, name)
            target = os.path.join(target_path, name)
            shutil.copy(source, target)


if __name__ == '__main__':
    img_path = "F:\\1.znzz\\2.Hisence-U-Tube\\1.ImageFiles\\Train_data\\20220328_pleats_Yolo5s_det_v4\\images"
    txt_path = "F:\\1.znzz\\2.Hisence-U-Tube\\1.ImageFiles\\Train_data\\20220212_pleats_Yolo_det_V3\\labels"
    target_path = "F:\\1.znzz\\2.Hisence-U-Tube\\1.ImageFiles\\Train_data\\20220328_pleats_Yolo5s_det_v4\\classes"
    get_txt(img_path, txt_path, target_path)

    pass
