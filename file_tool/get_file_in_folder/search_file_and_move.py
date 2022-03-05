#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/25 18:19
# @Author  : Wang Zixv
# @Site    : 
# @File    : search_file_and_move.py
# @Software: PyCharm

'''
在对应文件夹中查找所有类型的文件并根据目录移动到对应的文件夹中
程序调用时需要添加一下参数
文件后缀名称
查找文件的根目录
需要复制文件的根目录
'''
import os
import sys

import cv2

'''
获取包含图片的文件夹路径
'''


def get_file_contents(dir_name, _path_list, target_type):
    for root, dirs, files in os.walk(dir_name):
        # 遍历文件
        for dir in dirs:
            path = os.path.join(root, dir)
            data_folder = os.listdir(path)
            for path_1 in data_folder:
                data_folder_2 = os.listdir(path_1)
                data_folder_root = os.path.join(os.path.join(root, path_1), data_folder_2)
                if os.path.isdir(data_folder_root):
                    for img_file in data_folder_2:
                        img_path = os.path.join(data_folder_2, img_file)
                        if img_path.endswith(target_type):
                            path_list.append(img_path)
    return _path_list


def get_file_contents_2(dir_name, _path_list, target_type):
    for root, dirs, files in os.walk(dir_name):
        # 遍历文件

        for img_file in files:
            img_path = os.path.join(root, img_file)
            if img_path.endswith(target_type):
                _path_list.append(img_path)
    print(_path_list)
    return _path_list


"""
move images to target_file_path
"""


def move2file(path_list, target_file_path, split_all):
    if not os.path.exists(target_file_path):
        os.mkdir(target_file_path)

    i = 0
    for path in path_list:
        img_name = path.split("\\")
        img = cv2.imread(path)
        move_path = target_file_path
        # 筛选裁剪的图片和未裁剪的图片
        # if img.shape[0] < 2000:

        # if path.__contains__("cut_img"):
        #
        #     # 按照文件夹名称创建文件夹并进行分类
        #     name_list = ["ceju_img", "duibi_img", "luowen_huajian_img", "suokou_img", "hanjie_img", \
        #                  "chicun_img", "hanjie_img", "huajian_img", "yamaokahuang_img"]
        #     for name in name_list:
        #         if path.__contains__(name):
        #             move_path = os.path.join(target_file_path, name)
        #             break
        # else:
        #     move_path = os.path.join(target_file_path, "original_image")

        # 筛选图片
        # ********************************************************************************

        # # todo False 未能进行正确传递
        # if split_all == True:
        #     if path.__contains__("cut_img"):
        #
        #         # 按照文件夹名称创建文件夹并进行分类
        #         name_list = ["ceju_img", "duibi_img", "luowen_huajian_img", "suokou_img", "hanjie_img", \
        #                      "chicun_img", "hanjie_img", "huajian_img", "yamaokahuang_img"]
        #         for name in name_list:
        #             if path.__contains__(name):
        #                 move_path = os.path.join(target_file_path, name)
        #                 break
        #     else:
        #         move_path = os.path.join(target_file_path, "original_image")
        # else:
        #     # 只筛选花键
        #     # 即东项目二号台为小相机拍摄，图片为2448*2048 且命名为 0.jpg
        #     print("inside line 87 ")
        #     if path.__contains__("0.jpg") and not path.__contains__("cut_img"):
        #         print(path)
        #         move_path = target_file_path
        #     else:
        #         continue
        # ********************************************************************************
        # 只筛选花键
        # 即东项目二号台为小相机拍摄，图片为2448*2048 且命名为 0.jpg
        print("inside line 87 ")
        if path.__contains__("0.jpg") and not path.__contains__("cut_img"):
            print(path)
            move_path = target_file_path
        else:
            continue

        if not os.path.exists(move_path):
            os.mkdir(move_path)
        cv2.imwrite(move_path + "\\" + str(i) + ".jpg", img)
        i += 1


"""
参数：1.图片所在的文件夹路径  2.保存路径 3.是否全部筛选
"""
if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("参数缺少！请使用一下参数启动程序：0.程序名称 1.图片所在的文件夹路径  2.保存路径 3.是否全部筛选")

    path_list = []
    folder_path = sys.argv[1]
    save_path = sys.argv[2]
    # print(sys.argv[3])
    split_all_type = bool(sys.argv[3])

    # folder_path = "C:/Users/Admin/Desktop/station_1_20220105/sampling_photo/2022-01-05_test"
    # folder_path = "C:/Users/Admin/Desktop/test1"
    # save_path = "C:/Users/Admin/Desktop/station_1_20220105/sampling_photo/movetst_2"

    path_list = get_file_contents_2(folder_path, path_list, "jpg")
    print(path_list)
    move2file(path_list, save_path, split_all_type)
