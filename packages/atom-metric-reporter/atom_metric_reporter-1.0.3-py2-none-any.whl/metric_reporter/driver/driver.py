from appoptics import AppOptics
from datadog import DataDog


def new_driver(name, opts, log):
    """
        Create new driver

        :param opts: driver opts
        :type opts: dict
        :param opts: driver opts
        :type opts: dict
        :param log: logger instance
        :type log: object
    """

    drivers = {
        "appoptics": AppOptics,
        "datadog": DataDog
    }

    if name not in drivers:
        raise Exception("can't find driver name: " + name)

    driver = drivers[name]()

    driver.init(opts, log)
    return driver
