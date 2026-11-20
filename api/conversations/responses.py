from uuid import UUID

from pydantic import Field

from libs.datetime.utilities import to_iso_string
from libs.defaults.responses import BaseResponse

from .dtos import Conversation, ConversationMessage, ConversationSource, Usage


class UsageResponse(BaseResponse):
    input_tokens: int
    output_tokens: int
    total_tokens: int

    @classmethod
    def from_dto(cls, dto: Usage) -> "UsageResponse":
        return cls(
            input_tokens=dto.input_tokens,
            output_tokens=dto.output_tokens,
            total_tokens=dto.total_tokens,
        )


class ConversationSourceResponse(BaseResponse):
    chunk_index: int
    document_id: UUID
    id: UUID
    page_number: int | None
    reference: int
    source: str

    @classmethod
    def from_dto(cls, dto: ConversationSource) -> "ConversationSourceResponse":
        return cls(
            chunk_index=dto.chunk_index,
            document_id=dto.document_id,
            id=dto.id,
            page_number=dto.page_number,
            reference=dto.reference,
            source=dto.source,
        )


class ConversationMessageResponse(BaseResponse):
    created_at: str
    content: str
    conversation_id: UUID
    id: UUID
    model: str | None
    role: str
    sequence_number: int
    sources: list[ConversationSourceResponse] = Field(default_factory=list)
    usage: UsageResponse | None

    @classmethod
    def from_dto(cls, dto: ConversationMessage) -> "ConversationMessageResponse":
        return cls(
            created_at=to_iso_string(dto.created_at),
            content=dto.content,
            conversation_id=dto.conversation_id,
            id=dto.id,
            model=dto.model,
            role=dto.role,
            sequence_number=dto.sequence_number,
            sources=[ConversationSourceResponse.from_dto(dto=source) for source in dto.sources],
            usage=UsageResponse.from_dto(dto=dto.usage) if dto.usage else None,
        )


class ConversationResponse(BaseResponse):
    active: bool
    created_at: str
    id: UUID
    title: str
    updated_at: str

    @classmethod
    def from_dto(cls, dto: Conversation) -> "ConversationResponse":
        return cls(
            created_at=to_iso_string(dto.created_at),
            active=dto.active,
            id=dto.id,
            title=dto.title,
            updated_at=to_iso_string(dto.updated_at),
        )


class ConversationWithMessagesResponse(ConversationResponse):
    messages: list[ConversationMessageResponse] = Field(default_factory=list)

    @classmethod
    def from_dto(cls, dto: Conversation) -> "ConversationWithMessagesResponse":
        return cls(
            **ConversationResponse.from_dto(dto=dto).model_dump(),
            messages=[ConversationMessageResponse.from_dto(dto=message) for message in dto.messages],
        )
