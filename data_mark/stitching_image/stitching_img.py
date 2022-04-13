#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/18 17:57
# @Author  : Wang Zixv
# @Site    : 
# @File    : stitching_img.py
# @Software: PyCharm


import os
import subprocess
import time
import shutil


'''
获取包含图片的文件夹路径
'''


def get_file_contents(dir_name, pathList):
    for root, dirs, files in os.walk(dir_name):
        # 遍历文件
        for dir in dirs:
            path = os.path.join(root, dir)
            # todo 根据数量判断是否包含图片，判断逻辑不严谨，后期进行优化
            if len(os.listdir(path)) > 10:
                # path为文件路径，封装在listPath中返回
                pathList.append(path)

    return pathList


'''
组装运行算法 时的命令行中的参数
'''


def synthetic_run_command(language, func_name, img_folder_list, second_arg=None):
    run_command = []
    for folder_path in img_folder_list:
        l = []
        l.append(language)
        l.append(func_name)
        l.append(folder_path)
        if second_arg is not None:
            l.append(second_arg)
        run_command.append(l)
    return run_command


def run_algorithm(dir_path, folder_path, target_path, language, func_name, second_arg):
    part_path = []
    # 获取所有放图片的文件夹的路径
    part_path = get_file_contents(dir_path, part_path)
    print(part_path)
    # 组装所有可执行语句
    run_command = synthetic_run_command(language, func_name, part_path, second_arg)


    for run in run_command:
        print("run info is :" + str(run))
        r = subprocess.Popen(run, \
                             # stderr=subprocess.PIPE,\
                             stdout=subprocess.PIPE).communicate()[0]


if __name__ == '__main__':
    dir_path = "C:\\Users\\Admin\\Desktop\\zhouqi\\raw-data"
    language = "python"
    func_name = "stitch.py"
    # befor_run = ['cd', '/d', 'E:\\progectlocation\\01.algorithm\\XingYeAutoParts\\03.tools_from_zhang.tech\\stitch']
    run_algorithm(dir_path, folder_path='', target_path='', language=language, func_name=func_name,second_arg=None)
