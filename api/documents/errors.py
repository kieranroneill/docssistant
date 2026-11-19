from api.platform.application.enums import ErrorCode
from api.platform.defaults.errors import BaseError


class DocumentPathDoesNotExistError(BaseError):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(ErrorCode.DOCUMENT_PATH_DOES_NOT_EXIST_ERROR, message or "documents path does not exist")
