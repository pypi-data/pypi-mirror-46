from threading import Thread

class ThreadServer:
    def __init__(self):
        self.server_thread = None
        self.running = False
        self.pause = 0

    def isRunning(self):
        return self.running

    def run(self, *args, **kwargs):
        """
        Server main function
        """
        pass

    def start(self, *args, **kwargs):
        if self.running:
            return
        self.running = True
        self.server_thread = Thread(target=self.run, args=args, kwargs=kwargs)
        self.server_thread.start()

    def stop(self):
        self.running = False



