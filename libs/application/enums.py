from enum import Enum


class ErrorCode(Enum):
    # chat
    CHAT_USER_CANCELLED = 2000
    CONVERSATION_NOT_FOUND_ERROR = 2004
    # documents
    DOCUMENT_NOT_FOUND_ERROR = 3004
    # http
    FIELD_REQUIRED_ERROR = 4007
    # internal
    INTERNAL_SERVER_ERROR = 5000
    # documents
    DOCUMENT_PATH_DOES_NOT_EXIST_ERROR = 7000
