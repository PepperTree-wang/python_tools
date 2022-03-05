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
    if not os.path.exists(_save_path):
        os.mkdir(_save_path)
    # cv2.imwrite(_save_path + "\\" + img_name + "_" + line_count + ".jpg",
    #             img[int(y - h / 2):int(y + h / 2), int(x - w / 2):int(x + w / 2), ])
    cv2.imwrite(_save_path + "\\" + img_name,
                img[int(y - h / 2):int(y + h / 2), int(x - w / 2):int(x + w / 2), ])
    pass


def get_txt_file_path(txt_folder_path):
    return os.listdir(txt_folder_path)


def get_img_path():
    pass


def get_img_name(txt_file_path):
    _img_name = txt_file_path.split("\\")[-1]
    _img_name = _img_name[:-4]
    _img_name = _img_name + ".jpg"
    return _img_name


def get_classes():
    pass


def gen_folder(root_path, folder_name):
    pass


#
# def test():
#     path = "../lockData/train/"
#     saved_path = "../lockData/train_rotate/"
#     images = os.listdir(path + "images")
#     labels = os.listdir(path + "labels")
#     # print(images)
#     for image in images:
#         # 输入图片
#         # print(os.path.join(path + "images", image))
#         img = cv2.imread(os.path.join(path + "images", image), 1)
#         # 原图像的高、宽、通道数
#         rows, cols, chnl = img.shape
#
#         # 读取txt    旋转坐标
#         data = []
#         if os.path.exists(path + "labels/" + image[:-4] + ".txt"):
#             for line in open(path + "labels/" + image[:-4] + ".txt", "r"):  # 设置文件对象并读取每一行文件
#                 line = line[:-1]
#                 line = line.split(" ")

"""
需要使用一下参数：1.img_folder 2.classes.txt_file_path 3.roi_txt_folder 4.save_img_folder
"""
if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("需要使用一下参数：1.img_folder 2.classes.txt_file_path 3.roi_txt_folder 4.save_img_folder")

    img_root = sys.argv[1]
    roi_txt_folder = sys.argv[3]
    # 获取所有标记的数据roi
    txt_file_list = get_txt_file_path(roi_txt_folder)
    save_path = sys.argv[4]

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
        if not os.path.exists(img_root + "\\" + img_name):
            continue
        img = cv2.imread(img_root + "\\" + img_name)
        # print(img)
        # 保存图片
        i = 0
        for line_count in open(txt_file_path, "r"):  # 设置文件对象并读取每一行文件
            line = line_count[:-1]
            line = line.split(" ")
            # 获取坐标位置
            cla, x, y, w, h = load_txt(line, img)

            # 保存图片
            save_img(save_path, img_name, str(i), img, cla, x, y, w, h)
            i += 1
