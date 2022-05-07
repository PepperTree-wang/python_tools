#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/6 17:18
# @Author  : Wang Zixv
# @Site    : 
# @File    : Image clarity assessment.py
# @Software: PyCharm

import cv2
import os
import sys
import shutil
from split_img_from_labelimg_yolo_type.yolo_detect_function import yolo_detect


def get_img_clarity():
    # imagePath = "F:\\1.znzz\\2.Hisence-U-Tube\\1.ImageFiles\\Production_sampling\\2022-3-28-5-5\\2022-03-18-17-06-22\\3.png"
    imagePath = "F:\\1111.jpg"
    imagePath2 = "F:\\2222.jpg"
    # "F:\1.znzz\2.Hisence-U-Tube\1.ImageFiles\Production_sampling\2022-3-28-5-5\2022-05-05-10-55-36\3.png"
    # imagePath ="F:\\1.znzz\\2.Hisence-U-Tube\\1.ImageFiles\\Production_sampling\\2022-3-28-5-5\\2022-05-05-10-55-36\\3.png"
    image = cv2.imread(imagePath2)
    cv2.imshow('asdfa', image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.Laplacian(gray, cv2.CV_64F).var()
    print('ai_hellohello.jpg blur:', result)
    cv2.waitKey(0)


def get_left_logo(img_path):
    # print(weights)
    name_list, pred_images, boxes = yolo_detect(img_path)
    img = cv2.imread(img_path)

    boxes = boxes[name_list[0]][0:2]
    if len(boxes) < 2:
        return []
    print('*'*30)
    print(boxes)
    print(len(boxes))
    print('*'*30)

    b1 = boxes[0]
    b2 = boxes[1]
    x0, x1, y0, y1 = b1[0], b1[1], b1[2], b1[3]
    if b1[0] > b2[0]:
        x0, x1, y0, y1 = b2[0], b2[1], b2[2], b2[3]
    # print(x0, x1, y0, y1)
    img_new = img[int(y0):int(y1), int(x0):int(x1)]
    # print(img_new)
    return img_new


def main(path, save_path, weights):
    im_folder_list = os.listdir(path)
    for folder in im_folder_list:
        print(f'当前检测的文件夹为： {folder}')
        folder_path = os.path.join(path, folder)
        img_path = os.path.join(folder_path, '3.png')
        if not os.path.exists(img_path):
            continue
        # get left logo with YOLO
        img = get_left_logo(img_path)
        if len(img) < 1:
            print(f'{folder_path}'
                  f'路径下RU图片yolo 检测失败！')
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        score = cv2.Laplacian(gray, cv2.CV_64F).var()
        print(f'清晰度： {score}')
        if score >= 20:
            _save_path = os.path.join(save_path, folder)
            if not os.path.exists(_save_path):
                shutil.copytree(folder_path, _save_path)


if __name__ == '__main__':
    path = "F:\\1.znzz\\2.Hisence-U-Tube\\1.ImageFiles\\Production_sampling\\2022-3-28-5-5"
    save_path = os.path.join(path, '../select-20')
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    weights = "F:\\1.znzz\\2.Hisence-U-Tube\\1.ImageFiles\\Production_sampling\\haixin_length_20220310_1024_yolo5s.pt"
    main(path, save_path, weights)
