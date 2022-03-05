import get_all_folder as g
import subprocess

def get_folder_path():
    path = [       'E:\\02.PhotoData\\XingYePhotoData\\01.factory_sampling_photo\\2021-08-31\\2021-08-31-14-24-00',
       'E:\\02.PhotoData\\XingYePhotoData\\01.factory_sampling_photo\\2021-08-31\\2021-08-31-14-28-25',
        'E:\\02.PhotoData\\XingYePhotoData\\01.factory_sampling_photo\\2021-08-31\\2021-08-31-14-32-07', ]
    return path


def get_terminal_print():
    path = get_folder_path()
    print(path[1])
    for i in range(len(path)):
        r = subprocess.Popen(['python', \
                              'C:\\Users\\Admin\\Desktop\\algorithm\\main.py',\
                              path[i], \
                              'E:\\progectlocation\\01.algorithm\\XingYeAutoParts\\Punch_detection_algorithm_historical_version\\beta_v4_3\\AZ9729514301.txt'\
                              ], \
                             # stderr=subprocess.PIPE,\
                             stdout=subprocess.PIPE).communicate()[0]

        f = open('run_all_photo_result.txt', 'wb')
        f.write(path[i])
        f.write(r)
        f.close()


if __name__ == '__main__':
    # g.get_file_path("E:\\02.PhotoData\\XingYePhotoData\\01.factory_sampling_photo")
    get_terminal_print()
