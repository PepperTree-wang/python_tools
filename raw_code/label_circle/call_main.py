# -*- coding: utf-8 -*-
import subprocess

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import sys
import glob
from os import path
import os
import cv2
import csv


# 创建csv文件，获取csv对象
def init_csv_file(title=None):
    # 打开文件，追加a
    out = open('label_info.csv', 'a', encoding="utf-8-sig", newline='')
    # 设定写入模式
    csv_write = csv.writer(out, dialect='excel')
    if title is not None:
        # 写入具体内容
        csv_write.writerow(title)

    print("csv init over")
    return out


# 向 csv文件中写入数据
def save_data(data_info, csv_object):
    # 设定写入模式
    csv_write = csv.writer(csv_object, dialect='excel')
    # 根据不同的数据类型
    if isinstance(data_info,list):
        print("star")
        csv_write.writerow(data_info)
    if isinstance(data_info,tuple):
        csv_write.writerows(data_info)
    print("Finish")



# 获取路径下所有图片文件
def get_all_photo_path(path):
    path_list = []
    for root,dirs,files in os.walk(path):
        for file in files:
            path_list.append(os.path.join(root,file))
    return path_list

if __name__ == '__main__':
    plt.close("all")
    warnings.filterwarnings("ignore")
    path = "E:\\progectlocation\\01.algorithm\\XingYeAutoParts\\01.training_data\\large_hole_training_data\\1"
    title = ['img_path','x','y','r','label']
    # 0:联排孔，1：大孔
    label = '1'
    # 获取路径下所有图片文件
    p_list = get_all_photo_path(path)
    # # 初始化csv文件
    # csv_obj = init_csv_file(title)
    global img
    # 循环调用获取圆孔信息的方法
    i = 0
    for photo_path in p_list:

        img = cv2.imread(photo_path, 1)
        print("开始检测图片：" + str(photo_path))
        run = ["python","main.py",photo_path]
        result = subprocess.Popen(run, \
                             # stderr=subprocess.PIPE,\
                             stdout=subprocess.PIPE).communicate()[0]
        result_str = str(result)
        result_str = result_str[2:13]
        result_str = os.path.split(photo_path)[1] + "," + result_str
        print(result_str)
        info = result_str.split(",")
        print(info)
        print(type(info))
        # 手动添加label
        info.append(label)
        # 将信息保存到csv文件中
        out = open('label_info.csv', 'a', encoding="utf-8-sig", newline='')
        # 设定写入模式
        csv_write = csv.writer(out, dialect='excel')
        csv_write.writerow(info)
        i += 1
        print("当前进度：" + str(i) + "/" + str(len(p_list)))