from performance.controller.performance_server import PerformanceServer
import os
import sys

class PerformanceManger(object):
    def __init__(self):
        _directory_working = os.path.split(os.path.abspath(sys.argv[0]))[0]
        self.output = "".join([_directory_working, os.sep, 'results'])
        print(self.output)
        # self.performance_service = None
        self.status = False

    def begin(self, device_id, save_path=None, package_process='', peformance_interal=5, hrof_interal=1800):
        """
        :param device_id: id of adb devices
        :param save_path: file path to save
        :param package_process: dump the heap of a process. The given <PROCESS> argument may be either a process name or pid
        :param peformance_interal: the interal of memory to get
        :param hrof_interal: the interal of hrof to get
        :return:
        """
        if save_path == None:
            save_path = self.output

        self.performance_service = PerformanceServer()
        self.performance_service.start(device_id, save_path, package_process, peformance_interal,hrof_interal)
        self.status = True

    def end(self):
        self.performance_service.stop()
        self.performance_service.setPause(1)
        self.status = False


    def getrunning(self):
        return self.status

