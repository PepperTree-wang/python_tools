#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/21 9:51
# @Author  : Wang Zixv
# @Site    : 
# @File    : test_code_from_web.py
# @Software: PyCharm
# code from : https://www.yumefx.com/?p=3163
import os

import cv2
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


if __name__ == '__main__':
    image1 = cv2.imread('./test1/11.jpg')
    root = "./test2"
    img_list = os.listdir(root)

    for img_path in img_list:
        print("***********************************************************")
        print(img_path)
        path = os.path.join(root, img_path)
        image2 = cv2.imread(path)

        d_dist = Hamming_distance(dHash(image1), dHash(image2))

        p_dist = Hamming_distance(pHash(image1), pHash(image2))

        a_dist = Hamming_distance(aHash(image1), aHash(image2))

        print('a_dist is ' + '%d' % a_dist + ', similarity is ' + '%f' % (1 - a_dist * 1.0 / 64))
        print('p_dist is ' + '%d' % p_dist + ', similarity is ' + '%f' % (1 - p_dist * 1.0 / 64))
        print('d_dist is ' + '%d' % d_dist + ', similarity is ' + '%f' % (1 - d_dist * 1.0 / 64))
        print("***********************************************************")