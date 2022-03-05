# zixv wang
# 20220225

# python = 3.7

import os
import shutil
import sys
import cv2

folder_path = "E:/02.PhotoData/haixin_U-tube/Laboratory_sampling/20220225/sampling_photo"
head_save = "E:/02.PhotoData/haixin_U-tube/Laboratory_sampling/HEADER"
leg_save = "E:/02.PhotoData/haixin_U-tube/Laboratory_sampling/LEG"

f_list = os.listdir(folder_path)
img_path = ""
result_path = ""

# for f in f_list:
#     img_list = os.listdir(os.path.join(folder_path,f))
#     for img in img_list:
#         if img.__contains__("2.png"):
#             result_path = head_save
#         if img.__contains__("3.png"):
#             result_path = leg_save
for root,dir,file in os.walk(folder_path):
    if file.__contains__("2.png"):
        result_path = head_save
    if file.__contains__("3.png"):
        result_path = leg_save
    print(root)
    print(dir)
    print(file)
    #


