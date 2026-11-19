import logging
import os


def get_logger() -> logging.Logger:
    logger = logging.getLogger("uvicorn")

    logger.setLevel(os.getenv("LOG_LEVEL", "ERROR").upper())

    for handler in logger.handlers:
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s"))

    return logger
