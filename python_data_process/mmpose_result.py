#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/22 10:44
# @Author  : Wang Zixv
# @Site    : 
# @File    : mmpose_result.py
# @Software: PyCharm
import numpy as np
import cv2

results = [
    [
        {'bbox': [473.0223, 337.36697, 772.0419, 474.29172, 0.9472724],
         'keypoints': [[7.3827405e+02, 3.6140454e+02, 8.9100927e-01],
                       [7.4608704e+02, 3.6921759e+02, 8.7135756e-01],
                       [7.4608704e+02, 3.6531110e+02, 8.1645906e-01],
                       [7.4218054e+02, 3.8875006e+02, 8.6422408e-01],
                       [7.3436749e+02, 3.6531110e+02, 5.7728684e-01],
                       [7.2264795e+02, 4.0828259e+02, 8.4255779e-01],
                       [7.0702197e+02, 3.7312408e+02, 8.3125275e-01],
                       [6.9920898e+02, 4.4344116e+02, 8.9727509e-01],
                       [6.6795691e+02, 3.6140454e+02, 7.9509532e-01],
                       [6.5233093e+02, 4.6297369e+02, 8.7464261e-01],
                       [6.4842438e+02, 3.5359155e+02, 8.0278230e-01],
                       [6.3670490e+02, 4.2000214e+02, 7.4365795e-01],
                       [6.2889185e+02, 3.9265662e+02, 7.8423083e-01],
                       [5.5857477e+02, 4.0828259e+02, 5.5431741e-01],
                       [5.8201379e+02, 3.5359155e+02, 4.9007314e-01],
                       [4.9216418e+02, 4.2390863e+02, 3.5248816e-01],
                       [4.9607074e+02, 4.2390863e+02, 4.5705664e-01]]
         }],
    [
        {'bbox': [473.0223, 337.36697, 772.0419, 474.29172, 0.9472724],
         'keypoints': [[2.3827405e+02, 3.6140454e+02, 8.9100927e-01],
                       [2.4608704e+02, 3.6921759e+02, 8.7135756e-01],
                       [2.4608704e+02, 3.6531110e+02, 8.1645906e-01],
                       [2.4218054e+02, 3.8875006e+02, 8.6422408e-01],
                       [2.3436749e+02, 3.6531110e+02, 5.7728684e-01],
                       [2.2264795e+02, 4.0828259e+02, 8.4255779e-01],
                       [2.0702197e+02, 3.7312408e+02, 8.3125275e-01],
                       [6.9920898e+02, 4.4344116e+02, 8.9727509e-01],
                       [6.6795691e+02, 3.6140454e+02, 7.9509532e-01],
                       [6.5233093e+02, 4.6297369e+02, 8.7464261e-01],
                       [6.4842438e+02, 3.5359155e+02, 8.0278230e-01],
                       [6.3670490e+02, 4.2000214e+02, 7.4365795e-01],
                       [6.2889185e+02, 3.9265662e+02, 7.8423083e-01],
                       [5.5857477e+02, 4.0828259e+02, 5.5431741e-01],
                       [5.8201379e+02, 3.5359155e+02, 4.9007314e-01],
                       [4.9216418e+02, 4.2390863e+02, 3.5248816e-01],
                       [4.9607074e+02, 4.2390863e+02, 4.5705664e-01]]}
    ]
]

img = cv2.imread("E:\\3152result.jpg")
cv2.imshow('ori', img)


def draw_rectangle():
    """
    通过宽高比放大bbox
    """
    for re in results:
        points = re[0]['keypoints']
        x = []
        y = []
        for i, p in enumerate(points):
            x.append(p[0])
            y.append(p[1])
            if i >= 4:
                break
        # print()
        # min_x, max_x, min_y, max_y = int(min(x) * 1.5), int(max(x) * 1.5), int(min(y) * 1.5), int(max(y) * 1.5)
        min_x, max_x, min_y, max_y = int(min(x)), int(max(x)), int(min(y)), int(max(y))
        # min_x1, max_x1, min_y1, max_y1 = int(min(points[:3][0])), int(max(points[:3][0])), \
        #                              int(min(points[:3][1])), int(max(points[:3][1]))
        # print(x)
        # print(y)
        # print('-----------')
        # print(points[:4][0])
        # print('-----------')

        # print(f'm:{m},max_x:{max_x}')
        print(min_x, max_x, min_y, max_y)
        # 生成最大框
        dif_x = max_x - min_x
        dif_y = max_y - min_y
        if (min(dif_x, dif_y) / max(dif_x, dif_y)) < 0.8:
            if (min(dif_x, dif_y) / max(dif_x, dif_y)) < 0.8:
                bias = int(abs(dif_y - dif_x) / 2) * 2
                if dif_y > dif_x:
                    min_x -= bias
                    max_x += bias
                    max_y += bias
                else:
                    min_y -= bias
                    max_y += bias
                    max_x += bias

        cv2.rectangle(img, (min_x, min_y), (max_x, max_y), (0, 255, 0), 1)
    cv2.imshow('after', img)
    cv2.waitKey(0)


# l = []
# for i in range(10):
#     l.append([(i, i), (i, i)])
# print(l)


def draw_rectangle_center():
    """

    :return:
    """
    for re in results:
        points = re[0]['keypoints']
        x = []
        y = []
        for i, p in enumerate(points):
            x.append(p[0])
            y.append(p[1])
            if i >= 4:
                break

        min_x, max_x, min_y, max_y = int(min(x)), int(max(x)), int(min(y)), int(max(y))

        print(min_x, max_x, min_y, max_y)
        # 生成最大框
        dif_x = max_x - min_x
        dif_y = max_y - min_y
        center_x = int(dif_x / 2)
        center_y = int(dif_y / 2)

        cv2.rectangle(img, (min_x, min_y), (max_x, max_y), (0, 255, 0), 1)
    cv2.imshow('after', img)
    cv2.waitKey(0)


if __name__ == '__main__':
    pass
