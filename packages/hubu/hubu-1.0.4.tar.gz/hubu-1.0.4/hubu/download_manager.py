import queue
import threading
from hubu.base import Base
from hubu.downloader import Downloader

class DownloadManager(Base):
    def __init__(self, workers):
        super(__class__, self).__init__()
        self.number_of_workers = workers
        self.__queue = queue.PriorityQueue()
        self.__lock = threading.Lock()
        self.threads = []

    def __enter__(self):
        self.__start_workers()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__clear_workers()

    def __start_workers(self):
        self.log.info('start workers')
        for i in range(0, self.number_of_workers):
            t = Downloader(i, self)
            t.start()
            self.threads.append(t)

    def __clear_workers(self):
        self.log.info('Clear workers')
        for i in range(0, self.number_of_workers):
            self.__queue.put(-1)
        for t in self.threads:
            t.join()

    def add(self, item):
        self.lock().acquire()
        self.queue().put(item)
        self.lock().release()

    def queue(self):
        return self.__queue

    def lock(self):
        return self.__lock

    def status_line(self):
        line = " ".join(["  {:s}{:6.2f}%  ".format(t.action_icon(), t.progress() * 100) for t in self.threads])
        self.log.info(f"[{self.queue().qsize()}] {line}")

