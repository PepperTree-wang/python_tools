# -*- coding: utf-8 -*-
import random

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import sys
import glob
from os import path
import os
import cv2

'''
生成dataFrame 数据
'''


def generate_dataframe():
    info = []
    for i in range(20):
        temp = []
        for i in range(4):
            temp.append(str(random.randint(0, 100)))
        info.append(temp)
    return info


'''
向csv文件中写入数据
'''


def write2csv(info):
    df = pd.DataFrame(info)
    df.to_csv("test.csv", mode="a")
    print("finish!")


'''
向csv文件中写入数据
'''


def write_csv(info):
    df = pd.DataFrame(info)
    df.to_csv("test.csv", mode="a")
    print("finish!")


def read(path):
    df = pd.read_csv(path)
    print(df.shape[0])

if __name__ == '__main__':
    # path = "test.csv"
    # read(path)
    # list = generate_dataframe()
    # write2csv(list)
    pass
