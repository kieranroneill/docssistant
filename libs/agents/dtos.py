from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass()
class ChatMessage:
    content: str
    role: str


@dataclass()
class ChatSource:
    chunk_index: int
    document_id: UUID
    page_number: int | None
    reference: int
    source: str


@dataclass()
class ChatResult:
    content: str
    created_at: datetime
    input_tokens: int
    model: str
    output_tokens: int
    role: str
    total_tokens: int
