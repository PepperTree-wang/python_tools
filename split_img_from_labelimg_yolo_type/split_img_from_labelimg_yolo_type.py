#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/4 16:20
# @Author  : Wang Zixv
# @Site    : 
# @File    : split_img_from_labelimg_yolo_type.py
# @Software: PyCharm

"""
用来对labelimg 标记的yolo 格式的图片的roi区域进行裁剪
"""
import sys
import cv2
import os


def load_txt(roi, img):
    rows, cols, chnl = img.shape
    cla = str(roi[0])
    x = cols * float(roi[1])
    y = rows * float(roi[2])
    w = cols * float(roi[3])
    h = rows * float(roi[4])
    # print(cla)

    return cla, x, y, w, h


def save_img(save_path, img_name, line_count, img, cla, x, y, w, h):
    _save_path = os.path.join(save_path, cla)
    print("sa")
    if not os.path.exists(_save_path):
        os.mkdir(_save_path)
    # cv2.imwrite(_save_path + "\\" + img_name + "_" + line_count + ".jpg",
    #             img[int(y - h / 2):int(y + h / 2), int(x - w / 2):int(x + w / 2), ])
    cv2.imwrite(_save_path + "\\" + img_name + "_" + line_count + ".jpg",
                img[int(y - h / 2):int(y + h / 2), int(x - w / 2):int(x + w / 2), ])




# 获取目录下所有的路径
def get_path(_root_path):
    _img_root, _roi_txt_folder, _save_path = "","",""
    path_list = os.listdir(_root_path)
    print(path_list)
    for _path in path_list:
        abs_path = os.path.join(_root_path,_path)
        if os.path.isdir(abs_path):
            if _path.__contains__("images"):
                _img_root = abs_path
            elif _path.__contains__("labels"):
                _roi_txt_folder = abs_path

    _save_path_name = "cut_save_path"
    _save_path = os.path.join(root_path,_save_path_name)
    if os.path.exists(_save_path):
        _save_path += "_"+str(len(path_list))
    os.mkdir(_save_path)
    return _img_root, _roi_txt_folder, _save_path




def get_img_name(txt_file_path):
    _img_name = txt_file_path.split("\\")[-1]
    _img_name = _img_name[:-4]
    # _img_name = _img_name + ".jpg"
    return _img_name


def get_classes():
    pass



"""
需要使用一下参数：1.img_folder 2.classes.txt_file_path 3.roi_txt_folder 4.save_img_folder
"""
if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     # print("需要使用标记数据所在的文件夹路径！")
    #     raise ValueError("需要使用标记数据所在的文件夹路径！")

    root_path = sys.argv[1]
    # 获取所有路径
    img_root, roi_txt_folder, save_path = get_path(root_path)

    # 获取所有标记的数据roi
    txt_file_list = os.listdir(roi_txt_folder)

    # txt_file_list = get_txt_file_path(
    #     "E:/02.PhotoData/Jidong/Data/Training_data/train_data_for_NEIZHOU_LUOWENHUAJIAN_20220104/YOLO/label/")
    # save_path = "E:\\progectlocation\\01.algorithm\python_tool\\split_img_from_labelimg_yolo_type\\retult"
    # img_root = "E:/02.PhotoData/Jidong/Data/Training_data/train_data_for_NEIZHOU_LUOWENHUAJIAN_20220104/YOLO/images"

    for txt_file_name in txt_file_list:
        # 跳过分类名称文件
        if txt_file_name.__contains__("classes.txt"):
            continue
        # txt_file_path = roi_txt_folder + txt_file_name
        txt_file_path = os.path.join(roi_txt_folder, txt_file_name)
        img_name = get_img_name(txt_file_path)
        img_path = img_root + "\\" + img_name + ".bmp"

        if not os.path.exists(img_path):
            continue
        img = cv2.imread(img_path)
        # print(img)
        # 保存图片
        i = 0
        for line_count in open(txt_file_path, "r"):  # 设置文件对象并读取每一行文件
            # print(open(txt_file_path, "r"))
            # print(line_count)
            line = line_count[:-1]
            line = line.split(" ")
            # 获取坐标位置
            cla, x, y, w, h = load_txt(line, img)

            # 保存图片
            save_img(save_path, img_name, str(i), img, cla, x, y, w, h)
            i += 1
        # print(i)
