from typing import Literal
from uuid import UUID

from api.platform.defaults.dtos import BaseDTO


class Usage(BaseDTO):
    input_tokens: int
    output_tokens: int
    total_tokens: int


class ConversationMessage(BaseDTO):
    created_at: str
    content: str
    conversation_id: UUID
    id: UUID
    model: str
    role: Literal["assistant", "user"]
    sequence_number: int
    usage: Usage


class Conversation(BaseDTO):
    active: bool
    created_at: str
    id: UUID
    messages: list[ConversationMessage]
    updated_at: str
