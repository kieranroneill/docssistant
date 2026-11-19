from logging import Logger


class BaseController:
    _logger: Logger

    def __init__(self, logger: Logger):
        self._logger = logger
