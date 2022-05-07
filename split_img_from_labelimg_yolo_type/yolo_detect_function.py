#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/6 17:51
# @Author  : Wang Zixv
# @Site    : 
# @File    : yolo_detect_function.py
# @Software: PyCharm


import os
import sys
from pathlib import Path

import cv2
import numpy as np
import torch
import torch.backends.cudnn as cudnn
from models.common import DetectMultiBackend
from utils.datasets import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from utils.general import (LOGGER, check_file, check_img_size, check_imshow, check_requirements, colorstr,
                           increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, time_sync


@torch.no_grad()
def detect(weights="E:\\progectlocation\\01.algorithm\\python_tool\\split_img_from_labelimg_yolo_type\\weights\\haixin_length_20220310_1024_yolo5s.pt",  # model.pt path(s)
           images='./test/teaching/',  # file/dir/URL/glob, 0 for webcam
           imgsz=[1024, 1024],  # inference size (pixels)
           conf_thres=0.5,  # confidence threshold
           iou_thres=0.45,  # NMS IOU threshold
           max_det=100,  # maximum detections per image
           classes=None,  # filter by class: --class 0, or --class 0 2 3
           agnostic_nms=False,  # class-agnostic NMS
           augment=False,  # augmented inference
           visualize=False,  # visualize features
           line_thickness=3,  # bounding box thickness (pixels)
           ):
    # Load model
    device = select_device('cpu')
    model = DetectMultiBackend(weights, device=device)
    stride, names, pt, jit, onnx, engine = model.stride, model.names, model.pt, model.jit, model.onnx, model.engine

    dataset1 = LoadImages(images, img_size=imgsz, stride=stride, auto=pt)  # teaching

    # Run inference
    model.warmup(imgsz=(1, 3, *imgsz))  # warmup

    pred_images = {}
    boxes = {}
    images = {}
    # 图片文件名和识别的标签
    name_list = []
    # teaching imgs
    dt, seen = [0.0, 0.0, 0.0], 0
    for path, im, im0s, vid_cap, s in dataset1:  # per image
        t1 = time_sync()
        im = torch.from_numpy(im).to(device)
        im = im.half() if False else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        t2 = time_sync()
        dt[0] += t2 - t1

        # Inference
        # visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
        pred = model(im, augment=augment, visualize=visualize)
        t3 = time_sync()
        dt[1] += t3 - t2

        # NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
        dt[2] += time_sync() - t3

        # Process predictions
        for i, det in enumerate(pred):  # per image
            seen += 1
            p, im0, frame = path, im0s.copy(), getattr(dataset1, 'frame', 0)
            # area 面积
            height, width, channel = im0.shape

            p = Path(p)  # to Path
            s += '%gx%g ' % im.shape[2:]  # print string
            annotator = Annotator(im0, line_width=line_thickness, example=str(names))
            im1 = im0.copy()
            if len(det):
                # print("det",det)
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
                length = len(det)
                k = 0
                # box坐标  置信度 类别
                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)  # integer class
                    label = f'{names[c]} {conf:.2f}'
                    # plot
                    annotator.box_label(xyxy, label, color=colors(c, True))
            images[p.name] = im1
            pred_images[p.name] = im0  # 要画出来的图片
            # print(det.numpy())
            boxes[p.name] = det.numpy()
            # 记录文件名和对应识别到的标签
            name_list.append(p.name)
            # Print time (inference-only)
            # LOGGER.info(f'{s}Done. ({t3 - t2:.3f}s)')
    # print("yolo code boxes:",boxes)
    return name_list, pred_images, boxes, images


def yolo_detect( img_path):
    name_list, pred_images, boxes, images = detect(images=img_path)
    return name_list, pred_images, boxes

if __name__ == '__main__':
    print('main')
