from fastapi import Request

from .dtos import Application


def get_application(request: Request) -> Application:
    return request.app.state.application
