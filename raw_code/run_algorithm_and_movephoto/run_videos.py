#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/24 11:52
# @Author  : Wang Zixv
# @Site    : 
# @File    : run_videos.py
# @Software: PyCharm




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





def get_video_path():
    pass


if __name__ == '__main__':
    pass