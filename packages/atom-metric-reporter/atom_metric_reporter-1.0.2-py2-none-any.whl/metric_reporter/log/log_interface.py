import abc


class ILog:
    """
       Abstract Base Class for Log
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def info(self, msg):
        pass

    @abc.abstractmethod
    def warning(self, msg):
        pass

    @abc.abstractmethod
    def error(self, msg):
        pass

    @abc.abstractmethod
    def debug(self, msg):
        pass