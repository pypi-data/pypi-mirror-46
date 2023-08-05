from log_interface import ILog


class Log(ILog):
    def __init__(self, logger):
        if logger is None:
            import logging
            logging.basicConfig()
            self._logger = logging.getLogger("metric_reporter")
            self._logger.setLevel(logging.INFO)
        else:
            self._logger = logger

    def info(self, msg):
        self._logger.info(msg)

    def warning(self, msg):
        self._logger.warning(msg)

    def error(self, msg):
        self._logger.error(msg)

    def debug(self, msg):
        self._logger.debug(msg)
