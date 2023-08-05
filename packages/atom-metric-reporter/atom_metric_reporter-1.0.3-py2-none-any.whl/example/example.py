from metric_reporter.metric_reporter import MetricReporter
from metric_reporter.log.log_interface import ILog


class TestLog(ILog):
    def info(self, msg):
        print msg

    def warning(self, msg):
        print msg

    def error(self, msg):
        print msg

    def debug(self, msg):
        print msg


if __name__ == "__main__":
    metric_reporter = MetricReporter("appoptics", {
            "token": "cc709fde5c5d056e338c7450e2954702483b672e58915839f48abf5662c9e9a4"
        }, 1, 10, "g8y3e", TestLog())

    for i in range(1, 100):
        print "send metric: " + str(i)
        metric_reporter.send("test_metric", i, {
            "test": "test"
        })

    metric_reporter.stop()
