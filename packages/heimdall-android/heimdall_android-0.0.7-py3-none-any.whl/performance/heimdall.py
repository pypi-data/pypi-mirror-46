import argparse
import sys
import os
import signal
import threading
from performance.manager import PerformanceManger

curPath = os.path.abspath(os.path.dirname(__file__))
print(curPath)
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


def main():
    """
    Command line main entry
    Start heimdall
    * start with multipart args
    ```
    heimdall3 -device_id   --save_path --package_process --peformance_interal --hrof_interal
    ```
    """
    parser = argparse.ArgumentParser(prog="heimdall3")
    parser.add_argument('-d', '--device_id', dest='device_id', help='Set device id to memory')
    parser.add_argument('-s', '--save_path', dest='save_path', help='Set path to save results', default='.')
    parser.add_argument('-p', '--package_process', dest='package_process', help='The given <PROCESS> argument may be either a process name or pid, default is "com.sankuai.meituan"', default='com.sankuai.meituan')
    parser.add_argument('-t1', '--peformance_interal', dest='peformance_interal', type=int, help='the interal of memory to get', default=5)
    parser.add_argument('-t2', '--hrof_interal', dest='hrof_interal',type=int, help='the interal of hrof to get', default=600)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    print(f'Read args: {args}')
    run(args)


def run(args: argparse.Namespace):
    p = PerformanceManger()
    p.begin(device_id=args.device_id, save_path=args.save_path, package_process=args.package_process, peformance_interal=args.peformance_interal, hrof_interal=args.hrof_interal)

    # stop event handler
    def signal_handler(signum, frame):
        p.end()
        threading.Event().set()
        print('!!!Ctrl-C pressed. heimadall stop!!!')
        os._exit(1)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


def debug():
    # use heimadall.debug to start plugin in debug mode
    # can pass args by sys.args
    main()
    # main thread loop
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_forever()
