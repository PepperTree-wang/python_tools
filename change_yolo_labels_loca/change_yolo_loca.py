#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/15 17:29
# @Author  : Wang Zixv
# @Site    : 
# @File    : change_yolo_loca.py
# @Software: PyCharm
import os
import cv2


def save_new_txt(labels, save_path):
    with open(save_path, "a+") as f:
        for _label in labels:
            # # print(_label)
            for l in _label:
                # # print(str(l))
                f.write(str(l))
            f.write("\n")


# 按照最大框修改途中的小框
def change_location(txt_path, img_shape):
    txt_content = []
    new_line = []

    img_h = float(img_shape[0])
    img_w = float(img_shape[1])
    # ROI 中最大的w：外侧框
    max_w = 0
    # 外框坐标所在位置
    border_label_index = -1
    # # print(img_shape)
    for line_count in open(txt_path, "r"):  # 设置文件对象并读取每一行文件

        # # print(open(txt_file_path, "r"))
        # # print(line_count)
        line = line_count[:-1]
        line = line.split(" ")  # eg:['0', '0.565063', '0.422685', '0.029053', '0.053704']
        # # print(line)
        cla, x, y, w, h = int(line[0]), float(line[1]), float(line[2]), float(line[3]), float(line[4])
        # # print(cla, x, y, w, h)
        # 分如果>1，则将分类设定为1
        if cla > 1:
            cla = 1
        x = int(x * img_w)
        y = int(y * img_h)
        w = int(w * img_w)
        h = int(h * img_h)
        new_line = cla, x, y, w, h
        # 获取最大的w，并找到对应行坐标
        # print("w is : ",w)
        if w > max_w:
            max_w = w
            border_label_index = border_label_index + 1
            # print("&&&&&&&&&&&&&&&&&&&&&&")
            # print(max_w)
            # print(border_label_index)
            # print("&&&&&&&&&&&&&&&&&&&&&&")
        elif w< max_w:
            border_label_index = border_label_index + 1
        # cla, x, y, w, h
        txt_content.append(new_line)  # [[][][]]二维数组
    border_label_index = len(txt_content) -1
    # print("txt_content",txt_content)
    # todo 其他标记位置的相对坐标并进行归一化
    new_label = []
    new_txt_content = []
    for _label in txt_content:

        # print("_label",_label)
        border_label = txt_content[border_label_index]

        l_l, l_x, l_y, l_w, l_h = _label[0], _label[1], _label[2], _label[3], _label[4]
        b_l, b_x, b_y, b_w, b_h = border_label[0], border_label[1], border_label[2], border_label[3], border_label[4]

        # 计算顶点坐标
        x_0 = b_x - int(b_w / 2)
        y_0 = b_y - int(b_h / 2)
        x_1 = b_x + int(b_w / 2)
        y_1 = b_y + int(b_h / 2)
        # 跳过最外侧label
        # print(l_w)
        # print(max_w)
        if l_w == max_w:
            # print("这里是border")
            continue
        # 将坐标进行归一化
        _l_x = '% .6f' % float((l_x - x_0) / b_w)
        _l_y = '% .6f' % float((l_y - y_0) / b_h)
        _l_w = '% .6f' % float(l_w / b_w)
        _l_h = '% .6f' % float(l_h / b_h)
        # todo test loca
        if float(_l_w) > 1.0 or float(_l_y) > 1.0 or float(_l_x) > 1.0 or float(_l_h) > 1.0:
            # print("*" * 30)
            # print("计算错误")
            # print( l_l, _l_x, _l_y, _l_w, _l_h)
            # print("*" * 30)
            return None, None,None, None,None

        new_label = l_l, _l_x, _l_y, _l_w, _l_h
        new_txt_content.append(new_label)




    # print("new_txt_content",new_txt_content)
    return new_txt_content, x_0, y_0, x_1, y_1


if __name__ == '__main__':
    txt_folder_path = "E:/09.progect_location/progectlocation/01.algorithm/python_tool/change_yolo_labels_loca/dataset/labels"
    images_folder_path = "E:/09.progect_location/progectlocation/01.algorithm/python_tool/change_yolo_labels_loca/dataset/images"
    txt_return_folder_path = "E:/09.progect_location/progectlocation/01.algorithm/python_tool/change_yolo_labels_loca/dataset/result/labels"
    img_return_path = "E:/09.progect_location/progectlocation/01.algorithm/python_tool/change_yolo_labels_loca/dataset/result/images"

    txt_path_list = os.listdir(txt_folder_path)
    img_path_list = os.listdir(images_folder_path)
    for txt_part_path in txt_path_list:
        txt_path = txt_folder_path + "/" + txt_part_path
        # 图片不存在，跳过
        img_name = txt_part_path[:-4] + ".jpg"
        img_path = images_folder_path + "/" + img_name
        if not os.path.exists(img_path):
            continue
        img = cv2.imread(img_path, 1)
        img_shape = img.shape  # h,w,c
        # print("imgshape",img_shape)
        small_labels, x_0, y_0, x_1, y_1 = change_location(txt_path, img_shape)
        if small_labels is None:
            continue
        result_txt_path = txt_return_folder_path + "/" + txt_part_path
        small_img = img[y_0:y_1, x_0:x_1, ]

        # print(y_0, y_1, x_0, x_1)
        # cv2.imshow("small", small_img)
        # cv2.waitKey(0)
        # print(img_return_path + "/" + img_name)
        # cv2.imwrite(img_return_path + "/" + img_name, small_img)
        save_new_txt(small_labels, result_txt_path)

