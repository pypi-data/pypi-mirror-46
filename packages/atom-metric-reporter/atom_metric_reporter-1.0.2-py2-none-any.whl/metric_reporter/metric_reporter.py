import hashlib
from threading import Thread, Lock
import time

from driver.driver import new_driver
from log.log import Log
from thread_pool.thread_pool import ThreadPool


class MetricReporter:
    """
        Metric Reporter. supports send() method.
    """

    def __init__(self, driver_name, driver_opts, flush_interval=60, max_metrics=100, prefix="", logger=None, send_pool_size=10):
        self._log = Log(logger)

        if driver_name is not None:
            self._driver = new_driver(driver_name, driver_opts, self._log)
        else:
            raise Exception("driver name is None")

        self._flush_interval = flush_interval
        self._max_metrics = max_metrics
        self._prefix = prefix

        self._metrics = dict()

        self._is_running = True
        self._lock = Lock()

        self._sender_pool = ThreadPool(send_pool_size, self._log)

        handler_thread = Thread(target=self._metric_handler)
        handler_thread.daemon = True
        handler_thread.start()

    def _safe_metric(self, name, value, tags):
        hash_key = self._calc_hash(name, tags)

        self._lock.acquire()
        if hash_key in self._metrics:
            metric = self._metrics[hash_key]
            metric["points"].append([self._get_time(), value])

            self._lock.release()
            if len(metric["points"]) != 0 and len(metric["points"]) >= self._max_metrics:
                self._flush(metric)
        else:
            metric = {
                "name": name,
                "points": list(),
                "tags": tags,
                "start_time": self._get_time()
            }

            metric["points"].append([self._get_time(), value])

            self._metrics[hash_key] = metric
            self._lock.release()


    @staticmethod
    def _get_time():
        return int(time.time())

    @staticmethod
    def _calc_hash(name, tags):
        hash_data = name

        hash_list = list()
        for key in tags:
            tag = tags[key]

            hash_list.append(tag)
            hash_list.append(key)

        hash_list.sort()

        for item in hash_list:
            hash_data += item

        return hashlib.md5(hash_data).hexdigest()

    def _metric_send(self, name, points, tags):
        self._log.info("Metric reporter: sending metrics data, points len: " + str(len(points)))
        err = self._driver.send(name, points, tags)
        if err is not None:
            self._log.error("Metric reporter: " + err)

    def _flush(self, metric):
        self._lock.acquire()

        name = metric["name"]
        points = metric["points"]
        tags = metric["tags"]

        metric["start_time"] = self._get_time()
        metric["points"] = list()

        self._sender_pool.add_task(self._metric_send, name, points, tags)

        self._lock.release()

    def _flush_all(self):
        for key in self._metrics:
            metric = self._metrics[key]

            if len(metric["points"]) > 0:
                self._flush(metric)

    def _metric_handler(self):
        while self._is_running:
            current_time = self._get_time()
            for key in self._metrics:
                metric = self._metrics[key]

                start_time = metric["start_time"]
                if current_time - start_time >= self._flush_interval:
                    self._log.info("Metric reporter: flush metric: " + metric["name"] + " from interval")
                    if len(metric["points"]) > 0:
                        self._flush(metric)

    def send(self, name, value, tags):
        if len(self._prefix) > 0:
            name = self._prefix + '.' + name

        self._safe_metric(name, value, tags)

    def stop(self):
        if not self._is_running:
            return

        self._log.info("Metric reporter: flush from stop")
        self._is_running = False
        self._flush_all()

        self._sender_pool.wait_completion()

