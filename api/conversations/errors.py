from libs.application.enums import ErrorCode
from libs.defaults.errors import BaseError


class ConversationNotFoundError(BaseError):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(ErrorCode.CONVERSATION_NOT_FOUND_ERROR, message or "Conversation not found")
