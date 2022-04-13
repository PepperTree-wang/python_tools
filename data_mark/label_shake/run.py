# -*- coding: utf-8 -*-

import os
import subprocess
import main
import time
import shutil
import cv2
import pandas as pd

'''
获取包含图片的文件夹路径
'''

def get_file_contents(dir_name):
    path_list = []
    for root, dirs, files in os.walk(dir_name):
        # 遍历文件
        for dir in dirs:
            path = os.path.join(root, dir)
            # todo 根据数量判断是否包含图片，判断逻辑不严谨，后期进行优化
            # print(path)
            if len(os.listdir(path)) > 80:
                # path为文件路径，封装在listPath中返回
                path_list.append(path)

    return path_list



'''
组装运行算法 时的命令行中的参数
'''

def synthetic_run_command(language, func_name, img_folder_list ,second_arg = None):
    run_command = []
    print(img_folder_list)
    print(type(img_folder_list))
    for folder_path in img_folder_list:
        l = []
        l.append(language)
        l.append(func_name)
        l.append(folder_path)
        if second_arg is not None:	
        	l.append(second_arg)
        run_command.append(l)
    return run_command


'''
运行算法并获取算法给出的图片
    dir_path:存放所有图片的路径
    language：命令行中执行的语言
    func_name：python 程序名称
    second_arg：算法的第二个参数
'''


def run_function(dir_path, language, func_name, second_arg = None):

    # 获取所有放图片的文件夹的路径
    part_path = get_file_contents(dir_path)
    # 组装所有可执行语句
    run_command = synthetic_run_command(language, func_name, part_path ,second_arg)
    i = 0
    for run in run_command:
        print("run info is :" + str(run))
        time1 = time.time()
        r = subprocess.Popen(run, \
                             # stderr=subprocess.PIPE,\
                             stdout=subprocess.PIPE).communicate()[0]
        time2 = time.time()
        print("run time is ：" + str(time2 - time1))
        f = open('run_all_photo_result.txt', 'a')
        photo_path = run[2]
        f.write(str(photo_path))
        f.write(str(r))
        f.close()
        print(str(r))
        print("已经标记：【" + str(i) + "/" + str(len(part_path)) + "】")
        i += 1
        try:
            path = "label.csv"
            df = pd.read_csv(path)
            print("当前csv文件中总行数为：" + str(df.shape[0]))
        except:
            print("未找到文件！")



if __name__ == '__main__':
	# 存放所有图片的路径
    dir_path = "E:\\PythonProject\\01.factory_photo_data\\01.xingYeAutoParts_taking_photo_factory"
    
    # 命令行中执行语句的语言种类
    language = "python"
    # 命令行中执行语句的python方法
    func_name = "main.py"   

    run_function(dir_path,language,func_name)