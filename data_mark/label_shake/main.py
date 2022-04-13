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

ix,iy = -1,-1
drawing = False

# the bounding box position of the selected section
wx1,wy1 = 0,0
wx2,wy2 = 0,0

# if the abnormal section has been selected via mouse
ifselected = False

img = []

# use mouse event to draw mouse event
def select_abnormal(event, x, y, flags, param):
	# example of reading variable via param
	start_x = param[0]

	r = 5

	# make the ix iy and drawing global
	# ix: end x pos of abnormal region
	# iy: end y pos of abnormal region
	global ix, iy, drawing, img, wx1,wy1, wx2,wy2, ifselected

	# make a img backup copy (prevent draw will be covered) 
	imgCopy = img.copy()

	# draw a mouse indicator
	cv2.circle(imgCopy, (x, y), r, (255, 0, 0), 3)

	# if the leftbutton is pressed
	if event == cv2.EVENT_LBUTTONDOWN:
		print("current position ({}, {})".format(x, y))

		ifselected = False
		drawing = True
		ix = x
		iy = y

	elif event == cv2.EVENT_MOUSEMOVE:
		if drawing == True:
			cv2.rectangle(imgCopy, pt1=(ix,iy), pt2=(x, y), color=(0,255,255),thickness=1)
		else:
			cv2.rectangle(imgCopy, pt1=(wx1,wy1), pt2=(wx2,wy2), color=(0,255,255),thickness=1)

	# if the leftbutton is released
	elif event == cv2.EVENT_LBUTTONUP:
		drawing = False
		cv2.rectangle(imgCopy, pt1=(ix,iy), pt2=(x, y), color=(0,255,255),thickness=1)
		wx1,wy1 = ix,iy
		wx2,wy2 = x, y
		ifselected = True

	# display the img copy (with rectangle)
	cv2.imshow('image', imgCopy)

# load img sequence
def load_frames(folder, format = "jpg"):
	img_list = glob.glob(folder + '/*.' + format)
	img_list.sort()

	return img_list

# get frame to display in current window
def get_cur_frame(img_list, start_pos, interval = 5, resize_ratio = 0.2):
	# end_pos: end index of image to display
	end_pos = start_pos+interval if start_pos+interval<len(img_list) else len(img_list)
	# img content in current window
	imgs = []
	# img file path in current window
	img_files = []
	for i in range(start_pos,end_pos):
		img = cv2.imread(img_list[i],1)

		if img is not None:
			imgs.append(img)
			img_files.append(img_list[i])

	frame = cv2.vconcat(imgs)
	frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

	# cur_width: used to record the abnormal section
	cur_width = frame.shape[1]
	
	# resize the image
	if resize_ratio != 1:
		width = int(frame.shape[1] * resize_ratio)
		height = int(frame.shape[0] * resize_ratio)
		dim = (width, height)
		frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

	return frame, cur_width, img_files

# "C:\Users\hanto\Google 云端硬盘\research\知造\兴业钢梁冲孔\Code\label_shake"
if __name__ == '__main__':

	plt.close("all")
	warnings.filterwarnings("ignore")

# 	if len(sys.argv) <2 :
# 		print("A border shake label tool. ")
# 		print("VERSION BETA v1.0")
# 		print("Please rerun the program with following format:")
# 		print("python main.py \{$TEST_IMAGE\} (OPTIONAL)\{$SAVED_FILE_NAME\}")
# 		exit(0)

	# print("press a key to start...")
	# print("press { to slide into next page")
	# print("press } to slide into previous page")
	# print("left button to select abnormal section")
	# print("press c to clear the selected section")
	# print("press esc to exit...")

	# img_list = load_frames("./testdata/test1/")
	img_list = load_frames(sys.argv[1])
    
	if len(sys.argv) == 3:
		filename = sys.argv[-1]
	else:
		filename = "./label.csv"

	k = 10000
	# isEnd = False
	interval = 10


	# image resize ratio for display
	resize_ratio = 0.4

	# use to save the label progress
	label_info = []

	# use to double check redundant label info
	prev_label = [0,0,0,0]

	# 
	start_pos = 0
	start_x = 0
	isEnd, isStart = False, False
	
	while k != 27 : # and isEnd == False:
		img, cur_width, _ = get_cur_frame(img_list, start_pos = start_pos, \
			resize_ratio = resize_ratio,interval = interval)

		# example of using param to pass the variables
		param = [start_x, start_x]
		# print(start_pos)
		# print(prev_pos)
		# print(param)

		cv2.setMouseCallback('image', select_abnormal, param)
		cv2.imshow('image', img)

		k= cv2.waitKey(0)

		if k == 27:   # wait for esckey to exit
			if len(label_info) >0:
				print(label_info)
				df = pd.DataFrame(label_info, columns = ['x_0','y_0','x_1','y_1'])
				df['img_seq'] = sys.argv[1][-30:len(sys.argv[1])]
				df.to_csv(filename,mode="a")
			else:	
				print("no label saved!")
		# {
		elif k == 93 or k == ord("d") or k == ord("D"):
			if not isEnd: 
				start_x += cur_width

			# start_pos = start_pos+interval if start_pos+interval<len(img_list) else start_pos
			if start_pos+interval<len(img_list):
				start_pos = start_pos+interval 
				isEnd, isStart = False, False
			else:
				start_pos = start_pos
				isEnd, isStart = True, False

			print("start x: {}, start pos: {}".format(start_x, start_pos))

			wx1,wy1 = 0,0
			wx2,wy2 = 0,0
			ifselected = False

		# }
		elif k == 91 or k == ord("a") or k == ord("A"):
			if not isStart: 
				start_x -= cur_width
			
			if start_pos-interval>0:
				start_pos = start_pos-interval  
				isEnd, isStart = False, False
			else:
				start_pos = 0
				isEnd, isStart = False, True
			
			print("start x: {}, start pos: {}".format(start_x, start_pos)) 
			
			wx1,wy1 = 0,0
			wx2,wy2 = 0,0
			ifselected = False

		elif k == ord('c') or k == ord("C"):
			print("the selected section is cleared")
			wx1,wy1 = 0,0
			wx2,wy2 = 0,0
			ifselected = False

		elif k == ord('s') or k == ord("S"):
			if ifselected:
				# calculate the final position
				cur_label = [int(wx1/resize_ratio)+start_x,int(wy1/resize_ratio),\
					int(wx2/resize_ratio)+start_x,int(wy2/resize_ratio)]

				if cur_label != prev_label:
					print("the selected section is {},{} : {},{}".format(wx1,wy1,wx2,wy2))
					print("the selected section is saved")
					print(cur_label)

					label_info.append(cur_label)
					prev_label = cur_label
				else:
					print("you do not need to save same info for multiple times")
			else:
				print("you need to select the section first")
		# else:
		# 	continue

