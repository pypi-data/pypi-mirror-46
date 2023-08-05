import unittest
import responses

try:
    # python 3
    from urllib.parse import urlparse, quote
    from unittest.mock import MagicMock
except ImportError:
    # python 2
    from urlparse import urlparse
    from urllib import quote
    from mock import MagicMock

from metric_reporter.driver.driver import new_driver
from metric_reporter.log.log_interface import ILog


class MockLog(ILog):
    def info(self, msg):
        print msg

    def warning(self, msg):
        print msg

    def error(self, msg):
        print msg

    def debug(self, msg):
        print msg


class TestDriver(unittest.TestCase):
    def setUp(self):
        pass

    def test_wrong_name(self):
        exception = None
        try:
            new_driver("test", None, None)
        except Exception as ex:
            exception = ex

        self.assertNotEqual(exception, None)

    def test_appotics_wrong_opts(self):
        exception = None

        try:
            new_driver("appoptics", None, MockLog())
        except Exception as ex:
            exception = ex

        self.assertNotEqual(exception, None)

    def test_appoptics(self):
        expected_token = "Basic dGVzdDo="
        expected_url = "test"
        expected_timeout = 42

        exception = None
        driver = None
        try:
            driver = new_driver("appoptics", {
                "token": "test",
                "timeout": expected_timeout,
                "url": expected_url
            }, MockLog())
        except Exception as ex:
            exception = ex

        self.assertEqual(exception, None)

        self.assertEqual(driver._timeout, expected_timeout)
        self.assertEqual(driver._url, expected_url)

        self.assertEqual(driver._token, expected_token)


class TestAppopticsDriver(unittest.TestCase):
    def setUp(self):
        self.url = "http://test.com"
        self.driver = new_driver("appoptics", {
            "token": "test",
            "timeout": 42,
            "url": self.url
        }, MockLog())

    def test_collect_values(self):
        test_name = "test"
        test_values = [
            [1, 42],
            [1, 43]
        ]

        res = self.driver._collect_values(test_name, test_values)

        self.assertNotEqual(len(res), 0)

        test_metric = res[0]
        self.assertEqual(test_metric["count"], 2)
        self.assertEqual(test_metric["name"], test_name)
        self.assertEqual(test_metric["max"], 43)
        self.assertEqual(test_metric["min"], 42)

    @responses.activate
    def test_send(self):
        test_name = "test"
        test_values = [
            [1, 42],
            [1, 43]
        ]
        test_tags = {
            "test": "test"
        }

        responses.add(responses.POST, self.url, json={}, status=202)
        self.driver.send(test_name, test_values, test_tags)
