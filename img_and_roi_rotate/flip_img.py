#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/28 16:27
# @Author  : Wang Zixv
# @Site    : 
# @File    : flip_img.py
# @Software: PyCharm
import os
import cv2


def flip_images(img_path,result_path):
    name_list = os.listdir(img_path)
    for name in name_list:
        im_path = os.path.join(img_path, name)
        r_path = os.path.join(result_path,name)
        print(im_path)
        img = cv2.imread(im_path)
        img_f = cv2.flip(img, 0)
        cv2.imwrite(r_path, img_f)


if __name__ == '__main__':
    path = "F:\\1.znzz\\2.Hisence-U-Tube\\1.ImageFiles\\Laboratory_sampling\\20220317\\split"
    result_path = "F:\\1.znzz\\2.Hisence-U-Tube\\1.ImageFiles\\Laboratory_sampling\\20220317\\flip"
    flip_images(path,result_path)
