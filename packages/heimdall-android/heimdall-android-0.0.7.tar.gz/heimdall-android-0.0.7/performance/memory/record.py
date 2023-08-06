
import os
import time
import re
import subprocess

# from memory.memory.fileutil import get_current_time

count = 0
net_rcv_last = 0
net_snd_last = 0


def get_current_time(format='%Y-%m-%d %H:%M:%S'):
    __current_time = time.strftime(format)
    return __current_time


def ps_pid(device_id, process_name):
    pid_cmd = "adb -s %s shell ps -c" % (device_id)
    process_list = os.popen(pid_cmd)
    for line in process_list.readlines():
        if line.find(process_name) != -1:
            # line may be like this:
            # USER     PID   PPID  VSIZE  RSS     WCHAN    PC         NAME
            # root     5567  862   187736 19988   ffffffff 400422d8 S process_name
            process_info_list = line.split()
            return process_info_list[1]

    #If process_name process doesn't exist.
    return None

def pidof_pid(deviceid, package_name):
    pid_cmd = "adb -s %s shell pidof %s " % (deviceid, package_name)
    res = os.popen(pid_cmd)
    pid = res.read().strip("\n")
    return pid


def getUid(pid):
    uid_cmd = "adb shell cat /proc/%s/status | grep Uid" % (pid)
    ret = os.popen(uid_cmd)
    uidinfo = ret.read().strip("\n")
    uid =uidinfo.split()
    return uid[1]




def reset_battery(devices):
    cmd_history = "adb -s " + devices + " shell dumpsys batterystats --enable full-wake-history "
    cmd_reset = "adb -s " + devices + " shell dumpsys batterystats --reset"

    _cmd_history_ = subprocess.Popen(cmd_history, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd_history_info = _cmd_history_.stdout.readlines()

    _cmd_reset_ = subprocess.Popen(cmd_reset, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd_reset_info = _cmd_reset_.stdout.readlines()



def getBatteryFile(devices, file_path):
    cmd_7_battery = "adb -s " + devices + " bugreport " + file_path + os.sep + str(devices) + "_bugreport.zip"
    cmd_6_battery = "adb -s " + devices + " bugreport > " + file_path + os.sep + str(devices) + "_bugreport.txt"

    p1 = subprocess.Popen(cmd_6_battery, stdout=subprocess.PIPE,stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    (output6, err6) = p1.communicate()

    p2 = subprocess.Popen(cmd_7_battery, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          stdin=subprocess.PIPE, shell=True)

    (output7, err7) = p2.communicate()

def getBatteryInfo(devices):
    cmd = "adb -s " + devices + " shell dumpsys battery"
    output = subprocess.Popen(cmd, shell=True,
        stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.readlines()
    st = ".".join([x.decode() for x in output])
    battery2 = int(re.findall("level:.(\d+)*", st, re.S)[0])


def getBatterystatsByUid(uid,devices):
    cmd = "adb -s " + devices + " shell dumpsys batterystats com.baidu.duer.smartmate"
    output = subprocess.Popen(cmd, shell=True,
        stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.readlines()
    st = ".".join([x.decode() for x in output])


def get_cpukel(device_id):
    cpuinfo_cmd = "adb -s %s shell cat /proc/cpuinfo" % (device_id)
    cpuinfo_cmd = "adb -s " + device_id + " shell cat /proc/cpuinfo"
    output = os.popen(cpuinfo_cmd).read().split()
    sitem = ".".join([x.decode() for x in output])  # 转换为string
    return len(re.findall("processor", sitem))

def getTotalCpuTime(devices):
    '''
    user:从系统启动开始累计到当前时刻，处于用户态的运行时间，不包含 nice值为负进程。
    nice:从系统启动开始累计到当前时刻，nice值为负的进程所占用的CPU时间
    system 从系统启动开始累计到当前时刻，处于核心态的运行时间
    idle 从系统启动开始累计到当前时刻，除IO等待时间以外的其它等待时间
    iowait 从系统启动开始累计到当前时刻，IO等待时间(since 2.5.41)
    irq 从系统启动开始累计到当前时刻，硬中断时间(since 2.6.0-test4)
    softirq 从系统启动开始累计到当前时刻，软中断时间(since 2.6.0-test4)
    stealstolen  这是时间花在其他的操作系统在虚拟环境中运行时（since 2.6.11）
    guest 这是运行时间guest 用户Linux内核的操作系统的控制下的一个虚拟CPU（since 2.6.24）
    '''
    user = nice = system = idle = iowait = irq = softirq = 0
    cmd = "adb -s " + devices + " shell cat /proc/stat"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    res = output.split()
    for info in res:
        if info.decode() == "cpu":
            user = res[1].decode()
            nice = res[2].decode()
            system = res[3].decode()
            idle = res[4].decode()
            iowait = res[5].decode()
            irq = res[6].decode()
            softirq = res[7].decode()
            result = int(user) + int(nice) + int(system) + int(idle) + int(iowait) + int(irq) + int(softirq)
    return result


def getUserCpuTime(devices):
    '''
    user:从系统启动开始累计到当前时刻，处于用户态的运行时间，不包含 nice值为负进程。
    nice:从系统启动开始累计到当前时刻，nice值为负的进程所占用的CPU时间
    system 从系统启动开始累计到当前时刻，处于核心态的运行时间
    idle 从系统启动开始累计到当前时刻，除IO等待时间以外的其它等待时间
    iowait 从系统启动开始累计到当前时刻，IO等待时间(since 2.5.41)
    irq 从系统启动开始累计到当前时刻，硬中断时间(since 2.6.0-test4)
    softirq 从系统启动开始累计到当前时刻，软中断时间(since 2.6.0-test4)
    stealstolen  这是时间花在其他的操作系统在虚拟环境中运行时（since 2.6.11）
    guest 这是运行时间guest 用户Linux内核的操作系统的控制下的一个虚拟CPU（since 2.6.24）
    '''
    user = nice = system = idle = iowait = irq = softirq = 0
    cmd = "adb -s " + devices + " shell cat /proc/stat"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    res = output.split()
    for info in res:
        if info.decode() == "cpu":
            user = res[1].decode()
            result = int(user)
    return result


def getprocessCpuTime(pid, devices):
    """
    pid     进程号
    utime   该任务在用户态运行的时间，单位为jiffies
    stime   该任务在核心态运行的时间，单位为jiffies
    cutime  所有已死线程在用户态运行的时间，单位为jiffies
    cstime  所有已死在核心态运行的时间，单位为jiffies
    """
    utime = stime = cutime = cstime = 0
    cmd = "adb -s " + devices + " shell cat /proc/" + pid + "/stat"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    res = output.split()
    utime = res[13].decode()
    stime = res[14].decode()
    cutime = res[15].decode()
    cstime = res[16].decode()
    result = int(utime) + int(stime) + int(cutime) + int(cstime)
    return result


'''
计算两个时间点之间的CPU使用率
100*( processCpuTime2 – processCpuTime1) / (totalCpuTime2 – totalCpuTime1) (按100%计算，如果是多核情况下还需乘以cpu的个数);
cpukel cpu几核
pid 进程id
'''
def getBetweenCpuRate(pid, cpukel, devices):
    processCpuTime1 = getprocessCpuTime(pid, devices)
    totalCpuTime1 = getTotalCpuTime(devices)
    time.sleep(5)
    processCpuTime2 = getprocessCpuTime(pid, devices)
    totalCpuTime2 = getTotalCpuTime(devices)

    processCpuTime3 = processCpuTime2 - processCpuTime1
    # totalCpuTime3 = (totalCpuTime2 - totalCpuTime1)*int(cpukel)
    totalCpuTime3 = (totalCpuTime2 - totalCpuTime1)
    cpu = 100 * (processCpuTime3) / (totalCpuTime3)
    return (cpu)


'''
计算进程的CPU使用率
100* processCpuTime1) / (totalCpuTime);
cpukel cpu几核
pid 进程id
'''
def getUserCpuRate(devices):
    '''
        user:从系统启动开始累计到当前时刻，处于用户态的运行时间，不包含 nice值为负进程。
        nice:从系统启动开始累计到当前时刻，nice值为负的进程所占用的CPU时间
        system 从系统启动开始累计到当前时刻，处于核心态的运行时间
        idle 从系统启动开始累计到当前时刻，除IO等待时间以外的其它等待时间
        iowait 从系统启动开始累计到当前时刻，IO等待时间(since 2.5.41)
        irq 从系统启动开始累计到当前时刻，硬中断时间(since 2.6.0-test4)
        softirq 从系统启动开始累计到当前时刻，软中断时间(since 2.6.0-test4)
        stealstolen  这是时间花在其他的操作系统在虚拟环境中运行时（since 2.6.11）
        guest 这是运行时间guest 用户Linux内核的操作系统的控制下的一个虚拟CPU（since 2.6.24）
    '''

    user = nice = system = idle = iowait = irq = softirq = 0
    totalCpuTime = 0
    cmd = "adb -s " + devices + " shell cat /proc/stat"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    res = output.split()

    for info in res:
        if info.decode() == "cpu":
            user = res[1].decode()
            nice = res[2].decode()
            system = res[3].decode()
            idle = res[4].decode()
            iowait = res[5].decode()
            irq = res[6].decode()
            softirq = res[7].decode()
            totalCpuTime = int(user) + int(nice) + int(system) + int(idle) + int(iowait) + int(irq) + int(softirq)

    ctime = get_current_time()
    userRate = float(user) * 100 / float(totalCpuTime)
    return ctime + '\t'+ str(userRate)


'''
计算某进程的CPU使用率
100* processCpuTime1) / (totalCpuTime);
cpukel cpu几核
pid 进程id
'''
def getProcessCpuRate(pid, devices):
    processCpuTime = getprocessCpuTime(pid, devices)
    totalCpuTime = getTotalCpuTime(devices)
    cpuRate = 100 * float(processCpuTime) / float(totalCpuTime)
    return cpuRate



def getMeminfoByApp(deviceid, packagename):
    '''
    参数含义
    davik： davik使用的内存
    native：native堆上的内存，指c/c++堆内的内存
    other：除了davik和native的内存，包括c/c++堆内的内存
    Pss: 该内存指将共享内存按比例分配到使用共享内存的进程
    heap alloc： 已经使用的内存
    heap free： 空闲的内存
    share dirty： 共享，但是不能换页出去的内存
    private dirty： 非共享，🈶️不能换页出去的内存
    '''

    meminfo_cmd = "adb -s " + deviceid + " shell  dumpsys  meminfo  %s" % (packagename)
    ctime = get_current_time()
    mem_ret = os.popen(meminfo_cmd)
    mem_all_info = mem_ret.read()

    if 'No process found' not in mem_all_info:
        # r1 = re.compile(r"Native Heap\s{1,}\d{1,}")
        # r2 = re.compile(r"Dalvik Heap\s{1,}\d{1,}")
        # Nativeinfo = r1.findall(mem_all_info)[0]
        # Dalvikinfo = r2.findall(mem_all_info)[0]

        # Native memory
        p = re.compile(r"Native Heap\s{1,}\d{1,}.*\d{1,}")
        native_memory_detail = p.findall(mem_all_info)

        # dalvik_memory
        p = re.compile(r"Dalvik Heap\s{1,}\d{1,}.*\d{1,}")
        dalvik_memory_detail = p.findall(mem_all_info)

        r3 = re.compile(r"TOTAL\s{1,}\d{1,}")
        Totalinfo = r3.findall(mem_all_info)[0]
        Total = Totalinfo.split(" ")[-1]

        # get all memory info
        all_meminfo_cmd = "adb -s " + deviceid + " shell  dumpsys  meminfo "
        all_mem_ret = os.popen(all_meminfo_cmd)
        all_mem_info = all_mem_ret.read()

        r4 = re.compile(r"Total RAM:\s{1,}\d{1,}")
        allTotalinfo = r4.findall(all_mem_info)

        allTotal = allTotalinfo[0].split(':')[1]


        allTotalnum = int(allTotal)
        memRate = 100 * float(Total) / float(allTotalnum)

        if native_memory_detail and dalvik_memory_detail:
            p = re.compile(r"\d+")
            # native memory
            native_memory = p.findall(native_memory_detail[0])
            # dalvik_memory
            dalvik_memory = p.findall(dalvik_memory_detail[0])

            # info = ctime + '\t' + "native="+native_memory[0]+ '\t' + "dalvik="+dalvik_memory[0] + '\t' + "rate=" + str(memRate)
            info = ctime + '\t' + native_memory[0]+ '\t' +dalvik_memory[0] + '\t' + str(memRate) + '\n'

        else:
            info = ctime + '\t' + "0"  + '\t' + "0"  + '\t' + "0" + '\n'

    else:
        info = ctime + '\t' + "0" + '\t' + "0" + '\t' + "0" + '\n'

    return info

def run_command_have_result(run_cmd):
    popen = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    run_result =""
    while True:
        next_line = popen.stdout.readline()
        if popen.poll() is not None and not next_line:
            break
                # sys.stdout.write(next_line)
        if len(next_line) != 0:
            run_result += next_line
    popen.wait()
    return run_result

def get_serialno():
    get_devices_cmd = "adb devices".split(" ")
    run_result = run_command_have_result(get_devices_cmd)
    result = run_result.replace('List of devices attached','').replace('\n','').replace("\t","").replace('\r',"").replace(" ",'')
    devices_id  =  result.split('device')
    for serialno in devices_id:
        if len(serialno) == 0 or serialno.__contains__("?"):
            devices_id.remove(serialno)
    return devices_id


def sava_info(fpath, name, data):
    path = fpath  + os.sep + name + ".txt"
    info = open(path, "a+")
    try:
        info.write(str(data)+ "\n")
        info.flush()
        info.close()
    except:
        pass

