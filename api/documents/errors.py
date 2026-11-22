from libs.application.enums import ErrorCode
from libs.defaults.errors import BaseError


class DocumentNotFoundError(BaseError):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(ErrorCode.DOCUMENT_NOT_FOUND_ERROR, message or "document not found")
