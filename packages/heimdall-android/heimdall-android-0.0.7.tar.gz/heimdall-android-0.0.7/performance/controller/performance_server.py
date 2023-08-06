import codecs
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from performance.base.baseThread import ThreadServer
from performance.hrof.pull_hprof import activity_record, pull_hprof
from performance.memory.record import getMeminfoByApp, get_current_time


class PerformanceServer(ThreadServer):
    def __init__(self):
        super().__init__()
        self._executor = ThreadPoolExecutor(thread_name_prefix='PerformanceServer-')


    def run(self, device_id, save_path, package_process, peformance_interal,hrof_interal):
        print('run method running:',self.running, 'with parameter:', device_id, save_path, package_process, peformance_interal)
        input_path: Path = Path(save_path).expanduser().absolute()
        if not input_path.exists():
            input_path.mkdir(exist_ok=True)
        device_path = input_path / device_id
        if not device_path.exists():
            device_path.mkdir(exist_ok=True)
        gct = get_current_time('%Y%m%d_%H%M%S')
        time_path = device_path / gct
        if not time_path.exists():
            time_path.mkdir(exist_ok=True)

        self._executor.submit(self.meminfo, device_id, time_path, package_process, peformance_interal)
        self._executor.submit(self.hrofinfo, device_id, time_path, package_process, hrof_interal)
        self._executor.submit(self.activityinfo, device_id, time_path, hrof_interal)

    def meminfo(self, device_id, _path, package_process, interval):
        print('meminfo fun:', device_id, _path, package_process, interval, '\n')
        DEFAULT_FILENAME = 'meminfo.csv'
        conf_file = _path / DEFAULT_FILENAME
        memtitle = r'date' + '\t' + "native" + '\t' + "dalvik" + '\t' + "rate" + '\n'
        with codecs.open(conf_file, 'w+', 'utf-8') as f:
            f.write(memtitle)
        while self.pause:
            meminfo = getMeminfoByApp(device_id, package_process)
            print('meminfo:', meminfo)
            with codecs.open(conf_file, 'a+', 'utf-8') as f:
                f.write(meminfo)
            time.sleep(interval)
            if self.pause == 1:
                break


    def hrofinfo(self, device_id, _path, package_process, interval):
        print('hrofinfo fun:', device_id, _path, package_process, interval, '\n')
        while self.pause:
            pull_hprof(device_id, package_process, _path)
            time.sleep(interval)
            if self.pause == 1:
                break


    def activityinfo(self, device_id, _path, interval):
        print('activityinfo fun:', device_id, _path, interval, '\n')
        filename = _path / "activity_record.txt"
        while self.pause:
            activity_record(device_id, filename)
            time.sleep(interval)
            if self.pause == 1:
                break

    def start(self, device_id, save_path, package_process, peformance_interal,hrof_interal):
        if self.running:
            return
        self.running = True
        self.server_thread = threading.Thread(target=self.run, args=(device_id, save_path, package_process, peformance_interal, hrof_interal))
        self.server_thread.start()


    def setPause(self,value):
        self.pause = value