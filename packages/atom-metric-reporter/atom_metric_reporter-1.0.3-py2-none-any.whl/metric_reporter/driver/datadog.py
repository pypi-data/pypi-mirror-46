from metric_reporter.driver.driver_interface import IDriver


class DataDog(IDriver):
    """
        DataDog implementation of driver interface
    """

    def __init__(self):
        pass

    def init(self, opts, log):
        pass

    def send(self, name, values, tags):
        pass

