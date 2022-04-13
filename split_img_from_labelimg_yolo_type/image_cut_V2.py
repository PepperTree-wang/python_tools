# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
锁扣Detect
"""

import argparse
import json
import os
import sys
import time

from pathlib import Path

import cv2
import numpy as np
import torch
import torch.backends.cudnn as cudnn

from itertools import islice

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.datasets import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from utils.general import (LOGGER, check_file, check_img_size, check_imshow, check_requirements, colorstr,
                           increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, time_sync

"""
传入一个文件夹,返回yolo检测结果
@:return:
    name_list   图片文件名字列表
    pred_images     预测的图片.json格式,key为图片的名字,
    boxes   预测的box,json格式,key为图片的名字
"""


@torch.no_grad()
def detect(weights='E:/progectlocation/01.algorithm/python_tool/split_img_from_labelimg_yolo_type/weights/haixin-utube-distanceMeasure-bukabian-GPU-1024-20220217.pt',  # model.pt path(s)
           images='./test/teaching/',  # file/dir/URL/glob, 0 for webcam
           imgsz=[1024, 1024],  # inference size (pixels)
           conf_thres=0.1,  # confidence threshold
           iou_thres=0.1,  # NMS IOU threshold
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
            if len(det):
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
            pred_images[p.name] = im0  # 要画出来的图片
            boxes[p.name] = det.numpy()
            # 记录文件名和对应识别到的标签
            name_list.append(p.name)
            # Print time (inference-only)
            # LOGGER.info(f'{s}Done. ({t3 - t2:.3f}s)')
    return name_list, pred_images, boxes


def get_imgs_path(folder_path):
    path_list = []
    part_path = os.listdir(folder_path)
    for part in part_path:
        path_list.append(os.path.join(folder_path, part))

    return path_list

def main():
    opt = parse_opt()
    if_production, root, parameters = opt.if_production, opt.root, opt.parameters
    image_path, result_path = opt.image_path, opt.result_path
    weights = opt.weights


    if not os.path.exists(result_path):
        os.mkdir(result_path)
    imgs_path = get_imgs_path(image_path)
    print(opt)
    print(imgs_path)
    for img_path in imgs_path:
        name_list, pred_images, boxes = detect(weights=weights,images=img_path)

        # float -> int
        int_boxes = boxes[name_list[0]].astype(int)
        #  按照x_0坐标位置进行排序
        int_boxes = int_boxes[np.lexsort(int_boxes[:, ::-1].T)]

        img = cv2.imread(img_path)

        # 遍历坐标进行切图
        i = len(int_boxes)
        # # 判断检测数量是否为16个U管腿部或者8个U管顶部
        # if i != 16 or i != 8:
        #     print("*"*20)
        #     print("目标检测异常！")
        #     print(f"检测到的目标数量为：{i}")
        #     print("*"*20)
        for coordinate in int_boxes:
            x_0, y_0, x_1, y_1 = coordinate[0], coordinate[1], coordinate[2], coordinate[3]
            img_save_path = result_path + f"//{i}{name_list[0]}"
            print(img_save_path)
            cv2.imwrite(img_save_path, img[y_0:y_1, x_0:x_1, :])
            i -= 1





def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--if-production', default=True, action="store_true", help='if production: load json ;'
                                                                                   'else: load params')
    parser.add_argument('--root', type=str, default="E:/progectlocation/05.haixin_U-tube/03.python_algorithms/haixin_u-tube_algorithms",
                        help='root path')
    parser.add_argument('--parameters', type=str, default="parameters/foldDetection.txt", help='parameters in json')
    parser.add_argument('--weights', type=str, default="E:/progectlocation/05.haixin_U-tube/03.python_algorithms/haixin_u-tube_algorithms/measureDistance/measureDistance_lengthBiasDetect_v3.1/weights/haixin_length_20220310_1024_yolo5s.pt", help='yolo weights file')
    parser.add_argument('--image-path', type=str, default="F:\\1.znzz\\2.Hisence-U-Tube\\1.ImageFiles\\Train_data\\20220328_pleats_Yolo5s_det_v4\\big_img", help='path of images')
    parser.add_argument('--result-path', type=str, default="F:\\1.znzz\\2.Hisence-U-Tube\\1.ImageFiles\\Train_data\\20220328_pleats_Yolo5s_det_v4\\label_img", help='path of result images')
    opt = parser.parse_args()
    return opt


if __name__ == "__main__":
    t1 = time.time()
    main()
    t2 = time.time()
    print(f"time: {t2 - t1}")