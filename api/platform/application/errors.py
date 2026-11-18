from api.platform.defaults.errors import BaseError

from .enums import ErrorCode


class InternalServerError(BaseError):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(ErrorCode.INTERNAL_SERVER_ERROR, message or "Internal server error")
