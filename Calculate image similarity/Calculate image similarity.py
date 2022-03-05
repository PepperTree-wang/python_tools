#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/20 11:33
# @Author  : Wang Zixv
# @Site    : 
# @File    : Calculate image similarity.py
# @Software: PyCharm
# 计算图片相似度算法
import os
import sys
import skimage

import cv2
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def pHash(img, leng=32, wid=32):
    img = cv2.resize(img, (leng, wid))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dct = cv2.dct(np.float32(gray))
    dct_roi = dct[0:8, 0:8]
    avreage = np.mean(dct_roi)
    phash_01 = (dct_roi > avreage) + 0
    phash_list = phash_01.reshape(1, -1)[0].tolist()
    hash = ''.join([str(x) for x in phash_list])
    return hash


def dHash(img, leng=9, wid=8):
    img = cv2.resize(img, (leng, wid))
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
    hash = []
    for i in range(wid):
        for j in range(wid):
            if image[i, j] > image[i, j + 1]:
                hash.append(1)
            else:
                hash.append(0)
    return hash


def aHash(img, leng=8, wid=8):
    img = cv2.resize(img, (leng, wid))
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    avreage = np.mean(image)
    hash = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i, j] >= avreage:
                hash.append(1)
            else:
                hash.append(0)
    return hash


def Hamming_distance(hash1, hash2):
    num = 0
    for index in range(len(hash1)):
        if hash1[index] != hash2[index]:
            num += 1
    return num


def handle_img(img):
    img = cv2.resize(img, (100, 100))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])
    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    return img


def get_img_list(_target_folder):
    img_list = []
    for root, dirs, files in os.walk(_target_folder):
        for file in files:
            img_list.append(os.path.join(root, file))
    return img_list


# 直方图判断相似度
def get_similarity2(img_new, target_img_list, threshold_sim=0.5):
    for target_img_path in target_img_list:
        target_img = cv2.imread(target_img_path)
        if img_new.shape[0] == target_img.shape[0] and img_new.shape[1] == target_img.shape[1]:
            if img_new.shape[0] > 1000 or img_new.shape[1] > 1000:
                img1 = cv2.resize(img_new, (1000, 1000))
                img2 = cv2.resize(target_img, (1000, 1000))
            match2 = cv2.compareHist(img1, img2, cv2.HISTCMP_CORREL)
            # result_sim = cosine_similarity(img1, img2, dense_output=False)
            # result_sim_avg = np.mean(result_sim)
            print(match2)
            if match2 > threshold_sim:
                return True
    return False


# 图像哈希值判断相似度
def get_similarity3(img_new, target_img_list, threshold_sim=0.98):
    match2 = threshold_sim * 3
    # print(len(target_img_list))
    for target_img_path in target_img_list:
        # print(target_img_path)
        target_img = cv2.imread(target_img_path)
        d_dist = Hamming_distance(dHash(img_new), dHash(target_img))

        p_dist = Hamming_distance(pHash(img_new), pHash(target_img))

        a_dist = Hamming_distance(aHash(img_new), aHash(target_img))
        d = (1 - d_dist * 1.0 / 64)
        p = (1 - p_dist * 1.0 / 64)
        a = (1 - a_dist * 1.0 / 64)
        mean = d+p+a
        # print(mean)
        if mean == match2:
            return True
    return False


def get_similarity(img_new, target_img_list, threshold_sim=0.95):
    """
    余弦
    """
    img_new_gray = cv2.cvtColor(img_new, cv2.COLOR_BGR2GRAY)
    for target_img_path in target_img_list:
        target_img = cv2.imread(target_img_path)
        target_img_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
        # print(target_img_path)
        if img_new_gray.shape[0] == target_img_gray.shape[0] and img_new_gray.shape[1] == target_img_gray.shape[1]:
            # result_sim = compare_ssim(img_new, target_img, multichannel=True) # BUG
            if img_new_gray.shape[0] > 1000 or img_new_gray.shape[1] > 1000:
                img1 = cv2.resize(img_new_gray, (100, 100))
                img2 = cv2.resize(target_img_gray, (100, 100))
            # result_sim = cosine_similarity(img_new_gray, target_img_gray, dense_output=False)
            result_sim = cosine_similarity(img1, img2, dense_output=False)
            result_sim_avg = np.mean(result_sim)
            print(result_sim_avg)
            if result_sim_avg > threshold_sim:
                return True

    return False


def move_img(root_path, img_name, img):
    move_path = os.path.join(root_path, img_name)
    cv2.imwrite(move_path, img)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        # print("该算法")
        print("参数过少，请按照格式进行输入：0.python程序名称 1.准备移动的文件夹 2.目标文件夹")
        # todo break
    # move_folder = sys.argv[1]
    # target_folder = sys.argv[2]
    move_folder = "E:\\progectlocation\\python_program\\wallpaper\\Wallhaven"
    target_folder = "E:\\DesktopBackGround2"
    # move_folder = "./test1"
    # target_folder = "./test2"
    # 获取所有图片路径
    target_list = get_img_list(target_folder)
    move_list = get_img_list(move_folder)
    # 判断相似度
    i = 0

    for img_path in move_list:
        img_move = cv2.imread(img_path)
        result_bool = get_similarity3(img_move, target_list)
        if not result_bool:
            # 保存图片
            # img_name = str(img_path.split("\\")[-1:])
            img_name = str(len(os.listdir(target_folder))) + ".jpg"
            move_img(target_folder, img_name, img_move)
            print("移动了" + str(i) + " 张图片")
            i += 1
