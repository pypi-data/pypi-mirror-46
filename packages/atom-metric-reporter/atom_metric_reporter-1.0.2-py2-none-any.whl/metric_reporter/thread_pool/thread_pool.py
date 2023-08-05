try:
    # python 3
    from queue import Queue
except ImportError:
    from Queue import Queue

from threading import Thread


class Worker(Thread):
    """ Thread executing tasks from a given tasks queue """

    def __init__(self, tasks, log):
        Thread.__init__(self)
        self._log = log

        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                self._log.error(e)
            finally:
                self.tasks.task_done()


class ThreadPool:
    """ Pool of threads consuming tasks from a queue """

    def __init__(self, thread_num, log):
        if thread_num <= 0:
            thread_num = 1

        self.tasks = Queue(thread_num)

        for _ in range(thread_num):
            Worker(self.tasks, log)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        self.tasks.join()
