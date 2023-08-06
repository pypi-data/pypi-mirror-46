import os
import time
import subprocess

def pull_hprof(device_id, package_process, save_path):
    """
    :param device_id: id of adb devices
    :param package_process: dump the heap of a process.  The given <PROCESS> argument may be either a process name or pid
    :param save_path: file of save path
    :return:
    """
    print('save_path:', save_path)
    hrof2device_cmd = "adb -s %s shell am dumpheap %s /data/local/tmp/%s.hprof" % (device_id, package_process, device_id)
    print('hrof2device_cmd:', hrof2device_cmd)
    p1 = subprocess.Popen(hrof2device_cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE, shell=True)
    (output, err) = p1.communicate()
    time.sleep(10)
    datetime = time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
    hrof2pc_cmd = 'adb -s %s pull /data/local/tmp/%s.hprof  %s/%s_%s.hprof' % (device_id, device_id, save_path, device_id, datetime)
    print('hrof2pc_cmd:', hrof2pc_cmd)
    p2 = subprocess.Popen(hrof2pc_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    (output, err) = p2.communicate()
    _hprof_cnv = os.path.join(save_path,'_hprof_cnv')
    print('_hprof_cnv:', _hprof_cnv)
    if not os.path.exists(_hprof_cnv):
        os.makedirs(_hprof_cnv)
    time.sleep(5)
    conv_hprof = 'hprof-conv %s/%s_%s.hprof  %s/%s.hprof ' % (save_path, device_id, datetime, _hprof_cnv, datetime)
    print('conv_hprof:', conv_hprof)
    p3 = subprocess.Popen(conv_hprof, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          stdin=subprocess.PIPE, shell=True)
    (output, err) = p3.communicate()


def activity_record(device_id, record_filename):
    """
    :param device_id: id of adb devices
    :param record_filename: file name to save
    :return: None
    """
    _datetime = time.strftime("%Y%m%d %H:%M:%S ", time.localtime(time.time()))
    activities = os.popen("adb -s %s shell dumpsys activity activities | sed -En -e '/Running activities/,/Run #0/p'" % device_id)
    file_w = open(record_filename, 'a')
    file_w.writelines("===============================================================" + "\n")
    file_w.writelines(_datetime + "\n")
    file_w.writelines(activities)
    file_w.writelines("===============================================================" + "\n")
    file_w.close()



# pull_hprof('HT7131700092','com.sankuai.meituan','/Users/wangfuwen/Downloads')