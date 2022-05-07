#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/26 18:03
# @Author  : Wang Zixv
# @Site    : 
# @File    : Pick a marked image labels.py
# @Software: PyCharm
import os
import shutil

if __name__ == '__main__':
    folder_path = "F:\\1.znzz\\03.OldMan_Care\\01.datasets\\detection\\Shanmh_4.26\\ori"
    img_save_folder = "F:\\1.znzz\\03.OldMan_Care\\01.datasets\\detection\\Shanmh_4.26\\images2"
    txt_save_folder = "F:\\1.znzz\\03.OldMan_Care\\01.datasets\\detection\\Shanmh_4.26\\labels2"
    
    img_folder_name = "JPEGImages"
    txt_folder_name = "Annotations"
    folder_path_list = os.listdir(folder_path)
    i = 0
    for folder in folder_path_list:  # 三个分类
        folder_full_path = os.path.join(folder_path,folder)

        img_folder_path = os.path.join(folder_full_path, img_folder_name)
        txt_folder_path = os.path.join(folder_full_path, txt_folder_name)

        img_name_list = os.listdir(img_folder_path)
        for img_name in img_name_list:
            name = img_name.split('.')[0]
            txt_name = name + ".txt"

            img_path = os.path.join(img_folder_path, img_name)
            txt_path = os.path.join(txt_folder_path, txt_name)

            new_name = str(i)
            new_img_name = new_name + ".jpg"
            new_txt_name = new_name + ".txt"

            new_img_path = os.path.join(img_save_folder, new_img_name)
            new_txt_path = os.path.join(txt_save_folder, new_txt_name)

            # copy
            shutil.copy(img_path, new_img_path)
            shutil.copy(txt_path, new_txt_path)
            print(f"复制图片{img_path}和txt{txt_path} \n"
                  f"     到{new_img_path}和txt{new_txt_path}成功！")
            i += 1