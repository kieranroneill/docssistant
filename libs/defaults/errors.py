from fastapi import HTTPException

from libs.application.enums import ErrorCode


class BaseError(Exception):
    def __init__(self, code: ErrorCode, message: str) -> None:
        super().__init__(message)

        self.code: ErrorCode = code
        self.message: str = message

    def to_http_exception(self, status_code: int) -> HTTPException:
        return HTTPException(
            detail={
                "__isDSError": True,
                "code": self.code.value,
                "displayName": self.__class__.__name__,
                "message": self.message,
            },
            status_code=status_code,
        )
