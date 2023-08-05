import unittest

try:
    # python 3
    from urllib.parse import urlparse, quote
    from unittest.mock import MagicMock
except ImportError:
    # python 2
    from urlparse import urlparse
    from urllib import quote
    from mock import MagicMock

from metric_reporter.metric_reporter import MetricReporter


class TestMetricReporter(unittest.TestCase):
    def test_driver_name_none(self):
        exception = None
        try:
            MetricReporter(None, None)
        except Exception as ex:
            exception = ex

        self.assertNotEqual(exception, None)

    def test_metric_reporter_constructor(self):
        expected_interval = 42
        expected_max_metrics = 42
        expected_prefix = "test_prefix"

        exception = None
        metric_reporter = None
        try:
            metric_reporter = MetricReporter("appoptics", {
                "token": "test"
            }, expected_interval, expected_max_metrics, expected_prefix)
        except Exception as ex:
            exception = ex

        self.assertEqual(exception, None)

        self.assertEqual(metric_reporter._flush_interval, expected_interval)
        self.assertEqual(metric_reporter._max_metrics, expected_max_metrics)
        self.assertEqual(metric_reporter._prefix, expected_prefix)

    def test_metric_reporter_calc_hash(self):
        res = MetricReporter._calc_hash("test_name", {
            "test": "test"
        })

        self.assertEqual(res, "81de412c39d958f78f033cbbfd82e814")

    def test_metric_reporter_send(self):
        exception = None
        metric_reporter = None
        try:
            metric_reporter = MetricReporter("appoptics", {
                "token": "test"
            }, 10000, 10000, "test")
        except Exception as ex:
            exception = ex

        self.assertEqual(exception, None)

        expected_key = "f0498722996db03963cff6539b594d59"
        expected_name = "test.test"
        expected_tags = {
            "test": "test"
        }

        metric_reporter.send("test", 1, expected_tags)

        self.assertNotEqual(len(metric_reporter._metrics), 0)
        self.assertEqual(expected_key in metric_reporter._metrics, True)

        metric = metric_reporter._metrics[expected_key]

        self.assertEqual(metric["name"], expected_name)
        self.assertEqual(metric["tags"], expected_tags)