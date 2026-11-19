from uuid import UUID

from libs.defaults.dtos import BaseDTO


class ChatMessage(BaseDTO, frozen=True):
    content: str
    role: str


class ChatSource(BaseDTO, frozen=True):
    chunk_index: int
    document_id: UUID
    page_number: int | None
    reference: int
    source: str


class ChatResult(BaseDTO, frozen=True):
    content: str
    created_at: str
    input_tokens: int
    model: str
    output_tokens: int
    role: str
    total_tokens: int
