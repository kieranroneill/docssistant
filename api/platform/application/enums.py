from enum import Enum


class ErrorCode(Enum):
    # chat
    CHAT_USER_CANCELLED = 2000
    CONVERSATION_NOT_FOUND_ERROR = 2004
    # http
    FIELD_REQUIRED_ERROR = 4007
    # internal
    INTERNAL_SERVER_ERROR = 5000
