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


# get frame to display in current window
def get_cur_frame(df, idx):
	if idx <0:
		idx = len(df)
	row = df.iloc[idx]
	img_path = os.path.join(str(row['label']), row['img_path'])
	print(img_path)
	img = cv2.imread(img_path,1)
	cv2.circle(img, (row['x'], row['y']), row['r'], (255, 0, 0), 1)

	return idx, img, img_path

# "C:\Users\hanto\Google 云端硬盘\research\知造\兴业钢梁冲孔\Code\label_shake"
if __name__ == '__main__':

	plt.close("all")
	warnings.filterwarnings("ignore")

	print("press a key to start...")
	print("press D to slide into next page")
	print("press A to slide into previous page")
	print("press esc to exit...")

	df = pd.read_csv("./label_info_1_drop_error170.csv")

	k = 10000
	i = 0
	
	print("create")
	error_list = []

	while k != 27 : # and isEnd == False:
		i, img ,img_path= get_cur_frame(df, idx=i)

		cv2.imshow('image', img)

		k= cv2.waitKey(0)


		if k == 27:   # wait for esckey to exit
			exit(0)

		elif k == ord('a'):  
			i -= 1

		elif k == ord('d'):  
			i += 1

		elif k == ord('q'):  
			i -= 10

		elif k == ord('e'):  
			i += 10

		elif k == ord('s'):  
			f = open('error_cirl_2.txt', 'a')
			f.write(str(img_path))
			f.write(",")
			i += 1

	
