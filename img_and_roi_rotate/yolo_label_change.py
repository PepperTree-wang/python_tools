#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/26 15:45
# @Author  : Wang Zixv
# @Site    : 
# @File    : yolo_label_change.py
# @Software: PyCharm
# 调整yolo标注的结果

import os


def get_all_file_path(txt_ori, result_path):
    txt_name = os.listdir(txt_ori)
    txt_path_list = []
    txt_result_path = []
    for name in txt_name:
        txt_path_list.append(os.path.join(txt_ori, name))
        txt_result_path.append(os.path.join(result_path, name))
    return txt_path_list, txt_result_path


def change_value(txt_path, result_path):
    new_content = ""
    with open(txt_path, 'r') as t:
        content = t.readlines()
        print(content)
    for c in content:
        cont_list = c.split(' ')
        if len(cont_list) < 5:
            return

        new_content = new_content + cont_list[0] + " " + cont_list[2] + " " + cont_list[1] + " " + cont_list[4][:-2] + " " + cont_list[3] + "\n"
    print(new_content)
    with open(result_path, 'w') as r:
        r.writelines(new_content)
        print(f'{result_path}保存成功！')


if __name__ == '__main__':
    txt_ori = "F:\\1.znzz\\03.OldMan_Care\\01.datasets\\human detection dataset\\labels"
    result_path = txt_ori + "_new"
    if not os.path.exists(result_path):
        os.mkdir(result_path)
    txt_path_list, txt_result_path = get_all_file_path(txt_ori, result_path)
    for i, txt_path in enumerate(txt_path_list):
        change_value(txt_path, txt_result_path[i])
