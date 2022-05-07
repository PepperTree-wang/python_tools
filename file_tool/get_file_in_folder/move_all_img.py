#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/20 14:17
# @Author  : Wang Zixv
# @Site    : 
# @File    : move_all_img.py
# @Software: PyCharm
# 将文件中所有符合要求的图片拿出
import os
import sys
import shutil


def get_all_files(path, path_key_words):
    img_list = []
    for root, dirs, files in os.walk(path):
        # print(root)
        # print(dirs)
        for file in files:
            # print(file)
            if root.__contains__(path_key_words):
                img_list.append(os.path.join(root, file))
    return img_list


if __name__ == '__main__':
    path = "F:\\1.znzz\\2.Hisence-U-Tube\\1.ImageFiles\\Production_sampling\\head_top_img_save_path"
    key = "ori_image"
    target_folder_path = "F:\\1.znzz\\2.Hisence-U-Tube\\1.ImageFiles\\Production_sampling\\split"
    if not os.path.exists(target_folder_path):
        os.mkdir(target_folder_path)

    img_path_list = get_all_files(path, key)
    for path in img_path_list:
        if os.path.exists(path):
            file_name = str(len(os.listdir(target_folder_path))) + "." + path[-3:]
            file_path = os.path.join(target_folder_path, file_name)
            shutil.copy(path, file_path)
