#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/10 13:59
# @Author  : Wang Zixv
# @Site    : 
# @File    : get_keyboard_input.py
# @Software: PyCharm


import cv2
from distlib.compat import raw_input


if __name__ == '__main__':
    while True:
        k = 0
        k = ord("6")

        str = raw_input("Enter your input: ")
        print("Received input is : ", ord(str))


        # k = K_UP
        # k = cv2.waitKey()
        # print(k)

