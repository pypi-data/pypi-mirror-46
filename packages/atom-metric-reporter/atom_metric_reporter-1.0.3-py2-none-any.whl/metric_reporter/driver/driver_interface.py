import abc


class IDriver:
    """
       Abstract Base Class for driver
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def init(self, opts, log):
        """
       init driver instance

       :param opts: driver opts
       :type opts: dict
       :param log: logger instance
       :type log: object
       """
        pass

    @abc.abstractmethod
    def send(self, name, values, tags):
        """
        Add event (must to be synchronized)

        :param name: metric name
        :type name: str
        :param values: metric values
        :type values: list
        :param tags: metric tags
        :type tags: dict
        """
        pass