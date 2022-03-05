# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 10:39:05 2021

@author: Boyan
"""

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

# 将图片信息保存到csv文件中
def assemble_save_info(x,y,r):
    info = []
    # 获取图片文件名
    photo_name = os.path.split(str(sys.argv[1]))
    # 保存格式
    info.append(photo_name[1])
    info.append(x)
    info.append(y)
    info.append(r)
    return info

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
		# print("current position ({}, {})".format(x, y))
		# print("current r {}".format(r))
		global final_pos
		final_pos = [x,y,r]




plt.close("all")
warnings.filterwarnings("ignore")
circle_info = []

if len(sys.argv) <2 :
	print("A circle label tool. ")
	print("VERSION BETA v1.0")
	print("Please rerun the program with following format:")
	print("python main.py \{$TEST_IMAGE\} ")

img = cv2.imread(sys.argv[1],1)
k = 10000
r = 145
final_pos = []

# print("press a key to start...")
# print("press + to r+1")2222
# print("press p to r+10")
# print("press - to r-1")
# print("press o to r-10")
# print("press esc to exit...")
# if __name__ == '__main__':

while k != 27:
	cv2.setMouseCallback('image', drawCircle)
	cv2.imshow('image', img)
	k= cv2.waitKey(0)

	if k == 27:   # wait for esckey to exit
		if not final_pos :
			# print("you need to left click your mouse to select circle center first!")
			k = 10000
			continue
		else:
			cv2.destroyAllWindows()
			x,y,r = final_pos[0],final_pos[1],final_pos[2]
			result = str(x) + "," + str(y) + "," +str(r) + ", "
			print(result)
			sys.exit("current position ({}, {},{})".format(x, y,r))

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

