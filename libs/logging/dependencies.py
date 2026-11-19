from logging import Logger

from fastapi import Request


def get_logger(request: Request) -> Logger:
    return request.app.state.logger
