import os
import cv2


def get_video():
    cap = cv2.VideoCapture(0)
    i = 0
    img_list = []
    while (1):
        flag, frame = cap.read()
        cv2.imshow('f', frame)
        cv2.imwrite("./result.txt",frame)
        cv2.waitKey(0)

        img_list.append(frame)
        i += 1
        if i >= 200:
            return img_list, frame.shpe


def save(img_list, ori_size):
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    videoWrite = cv2.VideoWriter('output.mp4', fourcc, 24, ori_size)

    for img in img_list:
        videoWrite.write(img)
    videoWrite.release()


if __name__ == '__main__':
    img_list, shap = get_video()
    save(img_list, shap)
