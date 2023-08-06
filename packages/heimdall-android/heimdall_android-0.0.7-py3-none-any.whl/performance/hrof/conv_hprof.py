import os
import logging

def convHprofAll(dir_path):
    '''
    :param dir_path: 遍历目录的路径
    :return:
    '''
    if os.path.exists(dir_path):
        for dirpath, dirs, files in os.walk(dir_path, topdown=False):
            for file in files:
                if ".hprof" in file:
                    deviceid = file.split('_')[0]
                    save_dir = dir_path + '/' + deviceid + '_hprof_conv'
                    print('save_dir:', save_dir)
                    if not os.path.exists(save_dir):
                        print('xxxxxxxxxxxx')
                        os.makedirs(save_dir)
                    Abspath_dir = os.path.abspath(dirpath)
                    os.popen('hprof-conv %s/%s  %s/%s ' % (Abspath_dir, file,save_dir, file))
    else:
        logging.error("NO such dictionary, please try again ")


# if __name__ == '__main__':
#     # path = os.argv[0]
#     convHprofAll('/Users/wangfuwen/Downloads/f68ce080/20190114_190846')

