import os
import sys



def get_file_path(dir_name):
    listPath = []
    for root, dirs, files in os.walk(dir_name):
        # print(root)
        # print(dirs)
        # print(files)
        # 遍历文件
        for dir in dirs:
            path = os.path.join(root, dir)

            print(path)
            # path为文件路径，封装在listPath中返回
            listPath.append(path)

    return listPath


def get_file_name(dir_name):
    listFileName = []
    for root, dirs, files in os.walk(dir_name):
        # 遍历文件
        for file in files:
            # print(file)
            listFileName.append(file)

    return listFileName


if __name__ == "__main__":
    # 文件夹路径
    dirPath = "E:\\02.PhotoData\\XingYePhotoData\\01.factory_sampling_photo\\"
    listPath = get_file_path(dirPath)
    # listFileName = get_file_name(dirPath)
    # print(listPath)
    # print(listFileName)
    with open("folder_path.txt", "w") as  f:
        f.write(str(listPath))
