# -*- coding: utf-8 -*-
"""
Created on 2021-10-4

@author: Wang Zixv
"""
import os
import subprocess

import time
import shutil
import cv2

'''
获取包含图片的文件夹路径
'''


def get_file_contents(dir_name, pathList):
    for root, dirs, files in os.walk(dir_name):
        # 遍历文件
        for dir in dirs:
            path = os.path.join(root, dir)
            # todo 根据数量判断是否包含图片，判断逻辑不严谨，后期进行优化
            if len(os.listdir(path)) > 80:
                # path为文件路径，封装在listPath中返回
                pathList.append(path)

    return pathList


'''
组装运行算法 时的命令行中的参数
'''


def synthetic_run_command(language, func_name, img_folder_list,second_arg = None, ):
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


'''
将文件从当前路径移动到目标路径中
'''


def move_files(folder_path, target_path):
    # 检测文件路径是否存在
    if os.path.isfile(folder_path):
        print("该文件路径不存在！，文件路径为：" + folder_path)
        return
    # 检测目标路径是否存在
    if os.path.isfile(target_path):
        print("该文件路径不存在！，文件路径为：" + folder_path)
        if os.mkdir(target_path):
            print("创建路径成功！")
    file_path = os.listdir(folder_path)
    print("检测到当前文件夹下的文件个数为：" + str(len(file_path)))
    i = 0
    for file in file_path:
        old_name = os.path.join(folder_path, file)
        new_name = os.path.join(target_path, str(len(os.listdir(target_path))) + ".jpg")
        # 进行文件的移动
        shutil.move(old_name, new_name)
        print("移动第 【" + str(i) + "】 个文件，路径为：" + old_name)
        i += 1
    print("文件移动成功！")


'''
运行算法并获取算法给出的图片
    dir_path:存放所有图片的路径
    folder_path：想要移动内部数据的文件夹路径
    target_path：想要移动到的目标路径
    language：命令行中执行的语言
    func_name：python 程序名称
    second_arg：算法的第二个参数
'''


def run_algorithm(dir_path, folder_path, target_path, language, func_name, second_arg):
    part_path = []
    # 获取所有放图片的文件夹的路径
    part_path = get_file_contents(dir_path, part_path)
    # 组装所有可执行语句
    run_command = synthetic_run_command(language, func_name,part_path, second_arg )

    for run in run_command:
        print("run info is :" + str(run))
        time1 = time.time()
        r = subprocess.Popen(run, \
                             # stderr=subprocess.PIPE,\
                             stdout=subprocess.PIPE).communicate()[0]
        time2 = time.time()
        print("run time is ：" + str(time2 - time1))
        # 将图片移动到目标文件夹中
        move_files(folder_path, target_path)
        f = open('run_all_photo_result.txt', 'w')
        photo_path = run[2]
        f.write(str(photo_path))
        f.write(str(r))
        f.close()


'''
分离两种图片
'''


def separate_two_pictures(all_photo_path, one_path, more_path):
    # 遍历文件夹中的文件
    i = 0
    j = 0
    for root, dirs, files in os.walk(all_photo_path):
        for file in files:
            file_path = os.path.join(root, file)
            img = cv2.imread(file_path)
            if img.shape[1] > 400:
                new_name = one_path + "\\" + str(i) + ".jpg"
                i += 1
            else:
                new_name = more_path + "\\" + str(j) + ".jpg"
                j += 1

            print(new_name)
            shutil.move(file_path, new_name)


if __name__ == '__main__':
    # 存放所有图片的路径
    dir_path = "E:\\PythonProject\\01.factory_photo_data\\01.xingYeAutoParts_taking_photo_factory"
    # 存放所有截取出来的large的图片的路径
    folder_path = "E:\\PythonProject\\03.Python-algorithm\\znzz-XingYe-algorithm\\heatmap\\ROIs\\large"
    # 将图片进行移动的目标路径
    target_path = "E:\\PythonProject\\01.factory_photo_data\\02.training-data\\XingYeBigHole\\label"
    # 命令行中执行语句的语言种类
    language = "python"
    # 命令行中执行语句的python方法
    func_name = "main.py"
    # 命令行中执行语句的算法参数：第一个参数是图片文件夹路径
    second_arg = "E:\\PythonProject\\03.Python-algorithm\\znzz-XingYe-algorithm\\KH45B056AA.txt"
    # 声明所有图片的路径
    all_photo_path = "E:\\PythonProject\\01.factory_photo_data\\02.training-data\\XingYeBigHole\\test"
    # 单独一个孔位的路径
    one_path = "E:\\PythonProject\\01.factory_photo_data\\02.training-data\\XingYeBigHole\\0"
    # 连排空的路径
    more_path = "E:\\PythonProject\\01.factory_photo_data\\02.training-data\\XingYeBigHole\\1"

    # 运行算法并获取算法结果
    run_algorithm(dir_path, folder_path, target_path, language, func_name, second_arg)
    # 移动算法生成的文件
    move_files(folder_path, target_path)
    # 根据图片尺寸进行分类
    separate_two_pictures(all_photo_path, one_path, more_path)
