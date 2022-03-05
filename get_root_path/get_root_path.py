#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/29 8:30
# @Author  : Wang Zixv
# @Site    : 
# @File    : get_root_path.py
# @Software: PyCharm
import sys
import os

def get_root_path():
    print("zsdf")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("参数数量不足")
    argv0 = sys.argv[0]
    argv1 = sys.argv[1]
    argv2 = sys.argv[2]
    rootpath = os.getcwd()
    rootpath2 = os.getcwd()

    print("root1 " + rootpath)
    print("root2 " + rootpath2)

