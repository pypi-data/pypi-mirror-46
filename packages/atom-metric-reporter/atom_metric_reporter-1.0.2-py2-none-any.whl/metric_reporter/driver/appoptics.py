import base64
import requests
import json

from metric_reporter.driver.driver_interface import IDriver


class AppOptics(IDriver):
    """
        AppOptics implementation of driver interface
    """

    def __init__(self):
        self._log = None
        self._token = ""
        self._timeout = 60

        self._url = "https://api.appoptics.com/v1/measurements"

    def init(self, opts, log):
        self._log = log

        if opts is None or "token" not in opts or len(opts["token"]) <= 0:
            err = "AppOptics: error token empty!"
            self._log.error(err)
            raise Exception(err)

        if "url" in opts and len(opts["url"]) > 0:
            self._url = opts["url"]

        if "timeout" in opts and opts["timeout"] > 0:
            self._timeout = opts["timeout"]

        self._token = "Basic " + base64.b64encode(opts["token"] + ":")

    @staticmethod
    def _collect_values(name, values):
        values_map = dict()
        for value in values:
            key = value[0] - value[0] % 60

            if key in values_map:
                value_obj = values_map[key]
                value_obj["count"] += 1
                value_obj["sum"] += value[1]

                if value[1] < value_obj["min"]:
                    value_obj["min"] = value[1]

                if value[1] > value_obj["max"]:
                    value_obj["max"] = value[1]
            else:
                # init value
                value_obj = {
                    "name": name,
                    "period": 60,
                    "time": key,
                    "count": 1,
                    "sum": value[1],
                    "min": value[1],
                    "max": value[1],
                    "last": value[1],
                }

                values_map[key] = value_obj

        return values_map.values()

    def send(self, name, values, tags):
        if tags is None or len(tags.keys()) == 0:
            tags = {
                "general": "general"
            }

        new_tags = dict()
        for key in tags:
            tag = tags[key]
            if len(tag) > 0:
                new_tags[key] = tag.replace(" ", "_")
            else:
                self._log.warning("Metric reporter: tag key: " + key + " - is empty!")

        send_data = {
            "tags": new_tags,
            "measurements": self._collect_values(name, values)
        }

        headers = {
            "authorization": self._token,
            "content-type": "application/json"
        }

        try:
            response = requests.post(self._url, data=json.dumps(send_data), headers=headers, timeout=self._timeout)

            if response.status_code != 202:
                self._log.error("AppOptics: request error: " + response.content)
        except requests.exceptions.ConnectionError as ex:
            self._log.error("AppOptics: request exception: " + ex)
        except requests.exceptions.RequestException as ex:
            self._log.error("AppOptics: request exception: " + ex)


