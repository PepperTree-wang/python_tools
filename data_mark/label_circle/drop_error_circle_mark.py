#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-10-12
# @Author  : Zixv Wang

'''
用于删除数据标记过程中标记异常的数据的工具类
'''

import pandas as pd
import numpy as np


def get_error_circle_path(temp_error_file_path):
    f = open(temp_error_file_path)
    error = f.read()
    error_list = error.split(",")
    for i in range(len(error_list)):
        error_list[i] = error_list[i].strip()
    return error_list


def get_error_list(temp_error_file_path):
    f = open(temp_error_file_path)
    error = f.read()
    error_list = error.split(",")
    for i in range(len(error_list)):
        error_list[i] = error_list[i].strip()[2:len(error_list[i])]
    return error_list


def get_error_index(csv_path, error_list, column):
    circle_info = pd.read_csv(csv_path)
    index_list = []
    for column_content in error_list:
        try:
            result = circle_info.loc[circle_info[column] == column_content]
            # 先将数据框转换为数组
            result_array = np.array(result)
            result_array_list = result_array.tolist()
            img_raw = result_array_list[0]
            index = img_raw[0]
            print("result_array_list")
            print(index)
            # 其次转换为列表
            index_list.append(index)
        except:
            print("error")
    return index_list


def drop_error_line(csv_path, error_list):
    circle_info = pd.read_csv(csv_path)
    print(circle_info)
    # [9, 13, 18, 19, 24, 29, 36, 46, 50, 52, 55, 59, 60, 62, 65, 68, 69, 70, 71, 72, 74, 75, 78, 80, 81, 82, 83, 85, 86, 87, 88, 89, 91, 94, 100, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 119, 120, 121, 122, 123, 125, 126, 127, 129, 132, 133, 134, 135, 136, 137, 138, 139, 141, 142, 143, 144, 147, 148, 149, 150, 151, 152, 154, 155, 156, 158, 159, 160, 161, 162, 164, 165, 167, 170, 172, 173, 174, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 194, 192, 193, 194, 196, 197, 198, 199, 200, 201, 202, 203, 209, 210, 211, 216, 219, 220, 222, 223, 224, 226, 227, 228, 232, 239, 240, 242, 243, 244, 245, 249, 250, 252, 253, 254, 255, 256, 257, 258, 259, 261, 262, 263, 264, 265, 266, 267, 270, 272, 273, 274, 275, 279, 281, 283, 284, 285, 288, 289, 290, 294, 295, 296, 297, 299, 300, 302]
    # [2, 8, 9, 11, 15, 18, 19, 20, 23, 25, 28, 29, 30, 32, 33, 34, 35, 38, 39, 41, 46, 47, 53, 54, 55, 56, 58, 59, 63, 64, 65, 67, 68, 69, 75, 76, 77, 80, 81, 83, 84, 85, 87, 89, 90, 91, 92, 93, 94, 95, 96, 99, 100, 101, 102, 105, 107, 109, 113, 114, 115, 116, 122, 123, 125, 129, 131, 133, 135, 136, 137, 138, 141, 142, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 177, 178, 179, 180, 183, 184, 185, 186, 190, 191, 192, 194, 195, 196, 197, 198, 199, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 212, 213, 214, 215, 216, 217, 218, 219, 222, 223, 224, 225, 228, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 241, 242, 243, 244, 246, 249, 251, 251, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 262, 263, 264, 265, 266, 267, 268, 272, 273, 275, 276, 277, 278, 279, 280, 281, 282, 285, 287, 288, 289, 290, 291, 292, 293, 294, 295, 297, 298, 299, 301, 302, 304, 305, 307, 308, 310, 313, 314, 315, 316, 317, 318, 319, 322, 323, 324, 325, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 343, 344, 345, 346, 347, 352, 353, 354]
    # todo 这里在drop时，如果使用list作为参数进行传递，会出现错误
    circle_info = circle_info.drop(
        index=[2, 8, 9, 11, 15, 18, 19, 20, 23, 25, 28, 29, 30, 32, 33, 34, 35, 38, 39, 41, 46, 47, 53, 54, 55, 56, 58,
               59, 63, 64, 65, 67, 68, 69, 75, 76, 77, 80, 81, 83, 84, 85, 87, 89, 90, 91, 92, 93, 94, 95, 96, 99, 100,
               101, 102, 105, 107, 109, 113, 114, 115, 116, 122, 123, 125, 129, 131, 133, 135, 136, 137, 138, 141, 142,
               145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 163, 164, 165, 166,
               167, 168, 169, 170, 171, 172, 173, 174, 175, 177, 178, 179, 180, 183, 184, 185, 186, 190, 191, 192, 194,
               195, 196, 197, 198, 199, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 212, 213, 214, 215, 216, 217,
               218, 219, 222, 223, 224, 225, 228, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 241, 242, 243, 244,
               246, 249, 251, 251, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 262, 263, 264, 265, 266,
               267, 268, 272, 273, 275, 276, 277, 278, 279, 280, 281, 282, 285, 287, 288, 289, 290, 291, 292, 293, 294,
               295, 297, 298, 299, 301, 302, 304, 305, 307, 308, 310, 313, 314, 315, 316, 317, 318, 319, 322, 323, 324,
               325, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 343, 344, 345, 346, 347, 352, 353, 354])
    circle_info.to_csv(csv_path)
    print("drop and overwrite finished!")


if __name__ == '__main__':
    temp_error_file_path = "E:\\progectlocation\\01.algorithm\\XingYeAutoParts\\01.training_data\\large_hole_training_data\\row\\erroe_txt\\error_cirl_mark_2.txt"
    csv_path = "E:\\progectlocation\\01.algorithm\\XingYeAutoParts\\01.training_data\\large_hole_training_data\\label_info_1_drop_error170.csv"
    column = "img_path"
    # error_list = get_error_list(temp_error_file_path)
    # print("errorlist")
    # print(error_list)
    # index_list = get_error_index(csv_path, error_list, column)
    # print(index_list)
    # print(len(index_list))
    drop_error_line(csv_path, error_list = None)
