#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/13 17:50
# @Author  : Wang Zixv
# @Site    : 
# @File    : input_split_time.py
# @Software: PyCharm
import argparse
import cv2
import os
import json


def get_video_path(ori_folder, save_folder):
    """
    1.获取文件夹内的视频路径
    2.生成对应的文件保存路径
    :param ori_folder: 原始视频文件的路径
    :param save_folder: 裁剪后的视频的路径
    :return:  ori_paths: 所有视频的绝对路径 ;result_paths：对应视频保存的路径
    """
    v_list = os.listdir(ori_folder)
    if len(v_list) < 1:
        raise ValueError(f"该文件夹为空！文件夹路径为{ori_folder}")
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    ori_paths, result_paths = [], []
    for v in v_list:
        ori_paths.append(os.path.join(ori_folder, v))
        result_paths.append(os.path.join(save_folder, v))
    return ori_paths, result_paths


def nothing():
    pass


def get_frame(frame_index, video_cap):
    video_cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)  # 设置要获取的帧号
    flag, frame = video_cap.read()
    if not flag:
        raise ValueError(f'读取第{frame_index} 帧失败!')
    return frame


def split_video(video_path, type):
    json_content = ""
    video_cap = cv2.VideoCapture(video_path)
    frame_num = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 获取总帧数

    fps = video_cap.get(cv2.CAP_PROP_FPS)  # 获取视频的帧率

    # 新建一个窗口
    cv2.namedWindow('img')
    flag, frame = video_cap.read()
    # 新建一个滑动条
    cv2.createTrackbar('intensity', 'img', 0, frame_num, nothing)
    while (1):
        f_index = cv2.getTrackbarPos('intensity', 'img')
        frame = get_frame(f_index,video_cap)
        cv2.imshow('img', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()

    # 窗口中按下s记录一个开始点，按下e记录一个结束点同时显示一个下拉列表用于选择label
    # label 选择之后写入json中
    # 按下n跳到下一个视频
    return json_content


def save_video(img_list, save_path, ori_fps, ori_size):
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    videoWrite = cv2.VideoWriter('output.mp4', fourcc, ori_fps, ori_size)

    # todo for loop
    pass


def main(opt):
    # 加载参数
    video_folder = opt.video_folder
    classes_txt_path = opt.classes
    result_path = opt.result_path
    # 获取文件路径
    ori_paths, result_paths = get_video_path(video_folder, result_path)
    # load classes txt file
    with open(classes_txt_path, 'r') as cla:
        cla_list = cla.readline()

    i = 0
    while i < len(ori_paths):
        json_content = split_video(ori_paths[i], cla_list)

        i += 1

    # 完成所有视频遍历之后按照json进行视频裁剪

    pass


def get_parm():
    parser = argparse.ArgumentParser()
    parser.add_argument('--video-folder', type=str,
                        default="E:\\PythonProject\\02.python_tool\\python_tools\\video_cut\\split_video\\VIDEO",
                        help='video folder path')
    parser.add_argument('--classes', type=str, default='./classes.txt', help='video split classes')
    parser.add_argument('--result-path', type=str, default='./result', help='Save path after video clipping')

    opt = parser.parse_args()
    return opt


if __name__ == '__main__':
    opt = get_parm()
    main(opt)
