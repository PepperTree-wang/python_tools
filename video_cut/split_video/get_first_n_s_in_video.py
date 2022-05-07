#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/11 13:35
# @Author  : Wang Zixv
# @Site    : 
# @File    : get_first_n_s_in_video.py
# @Software: PyCharm
# 使用python进行视频前几秒的视频进行裁剪
import os
import sys
from moviepy.editor import *


def gen_video_name(save_folder_path):
    video_name_part = len(os.listdir(save_folder_path))
    video_name = str(len(os.listdir(save_folder_path))) + ".mp4"
    save_path = os.path.join(save_folder_path, video_name)

def get_video(start_time, end_time, video_path, save_folder_path):
    """
    裁剪视频对应时间内的帧
    """
    # clip = VideoFileClip(video_path).subclip(start_time, end_time)
    video = CompositeVideoClip([VideoFileClip(video_path).subclip(start_time, end_time)])
    # video_name = str(len(os.listdir(save_folder_path))) + "." + video_path.split(".")[-1]
    video_name_part = len(os.listdir(save_folder_path))
    video_name = str(len(os.listdir(save_folder_path))) + ".mp4"
    save_path = os.path.join(save_folder_path, video_name)
    print(save_path)
    while os.path.exists(save_path):
        video_name_part += 1
        video_name = str(video_name_part) + ".mp4"
        save_path = os.path.join(save_folder_path, video_name)
        if not os.path.exists(save_path):
            break
        print("123")

    video.write_videofile(save_path, fps=30, threads=1, codec="libx264")


def get_time_on_video_path(video_path):
    split = os.path.split(video_path)[-1]
    print(split)
    vide_n = split.split("_")
    start = vide_n[0]
    end = vide_n[1]
    return start, end

def get_time_arear_video(video_folder,save_folder):
    for video_name in video_path_list:
        video_path = os.path.join(video_folder, video_name)
        start_time, end_time = get_time_on_video_path(video_path)
        print("00000000000000000000000000000")
        print(start_time, end_time)
        get_video(start_time, end_time, video_path, save_folder)

def get_first_sec_in_video(video_folder,save_folder):
    for video_name in video_path_list:
        video_path = os.path.join(video_folder, video_name)
        start_time, end_time = 0,1
        get_video(start_time, end_time, video_path, save_folder)


if __name__ == '__main__':
    #
    # video_folder = "F:\\1.znzz\\03.OldMan_Care\\01.datasets\\datasets\\getUp"
    video_folder ="E:\\video\\test"
    save_folder = video_folder + "_split"
    video_path_list = os.listdir(video_folder)
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    get_time_arear_video(video_folder, save_folder)

