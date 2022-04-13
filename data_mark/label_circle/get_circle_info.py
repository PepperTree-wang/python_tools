# -*- coding: utf-8 -*-

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

# todo 方法中存在错误


circle_info = []
r = 150
img = None
'''
绘制圆环
'''
def drawCircle(event, x, y, flags, param):
	if event == cv2.EVENT_MOUSEMOVE:
		global circle_info
		global r
		circle_info = [x,y,r]

		imgCopy = img.copy()
		cv2.circle(imgCopy, (x, y), r, (255, 0, 0), 3)
		cv2.imshow('image', imgCopy)

	if event == cv2.EVENT_LBUTTONDOWN:
		print("current position ({}, {})".format(x, y))
		print("current r {}".format(r))
		global final_pos
		final_pos = [x,y,r]


# 获取图片的信息并将信息保存到csv文件中
def get_info_and_save(img_path):
    plt.close("all")
    warnings.filterwarnings("ignore")
    global circle_info
    global r
    circle_info = []

    k = 10000
    r = 150
    final_pos = []

    print("press a key to start...")
    print("press 1 to r+1")
    print("press p to r+10")
    print("press 2 to r-1")
    print("press o to r-10")
    print("press esc to exit and save ")

    while k != 27:
        cv2.setMouseCallback('image', drawCircle)
        print(type(img))
        cv2.imshow('image', img)
        k= cv2.waitKey(0)

        if k == 27:   # wait for esckey to exit
            if not final_pos :
                print("you need to left click your mouse to select circle center first!")
                k = 10000
                continue
            else:
                cv2.destroyAllWindows()
                x,y,r = final_pos[0],final_pos[1],final_pos[2]
                # todo save info to file
                info = assemble_save_info(img_path,x,y,r)
                return info
                # sys.exit("circle center ={},{}, r = {}".format(x,y,r))

        elif k == ord('='):
            r += 1

        elif k == ord('-'):
            r -= 1

        elif k == ord('p'):
            r += 10

        elif k == ord('o'):
            r -= 10
        elif k == ord('1'):
            r += 1
        elif k == ord('2'):
            r -= 1

# 将图片信息保存到csv文件中
def assemble_save_info(photo_path,x,y,r):
    info = []
    # 获取图片文件名
    photo_name = os.path.split(str(photo_path))
    # 保存格式
    info.append(photo_name)
    info.append(x)
    info.append(y)
    info.append(r)
    return info

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
        csv_write.writerow(data_info)
    if isinstance(data_info,tuple):
        csv_write.writerows(data_info)


# 获取路径下所有图片文件
def get_all_photo_path(path):
    path_list = []
    for root,dirs,files in os.walk(path):
        for file in files:
            path_list.append(os.path.join(root,file))
    return path_list
