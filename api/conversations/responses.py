from uuid import UUID

from pydantic import Field

from libs.datetime.utilities import to_iso_string
from libs.defaults.responses import BaseResponse

from .dtos import Conversation, ConversationMessage, ConversationSource, Usage


class UsageResponse(BaseResponse):
    input_tokens: int = Field(description="The number of input tokens that were used in the query")
    output_tokens: int = Field(description="The number of output tokens that were used in the response")
    total_tokens: int = Field(description="The total number of tokens that were used in the query and response")

    @classmethod
    def from_dto(cls, dto: Usage) -> "UsageResponse":
        return cls(
            input_tokens=dto.input_tokens,
            output_tokens=dto.output_tokens,
            total_tokens=dto.total_tokens,
        )


class ConversationSourceResponse(BaseResponse):
    chunk_index: int = Field(description="The index of the chunk that the source is from")
    document_id: UUID = Field(description="The id of the document that the source is from")
    id: UUID = Field(description="The id of the source")
    page_number: int | None = Field(description="The page number that the source is from")
    reference: int = Field(description="The reference number of the source")
    source: str = Field(description="The source, i.e. the URL of the document")

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
    created_at: str = Field(description="The timestamp of when the message was created")
    content: str = Field(description="The content of the message")
    conversation_id: UUID = Field(description="The id of the conversation that the message belongs to")
    id: UUID = Field(description="The id of the message")
    model: str | None = Field(description="The model that was used to generate the message")
    role: str = Field(description="The role of the message")
    sequence_number: int = Field(description="The sequence number of the message")
    sources: list[ConversationSourceResponse] = Field(
        default_factory=list, description="The sources that were used to generate the message"
    )
    usage: UsageResponse | None = Field(description="The usage of the message")

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
    active: bool = Field(description="Whether the conversation is active")
    created_at: str = Field(description="The timestamp of when the conversation was created")
    id: UUID = Field(description="The id of the conversation")
    title: str = Field(description="The title of the conversation")
    updated_at: str = Field(description="The timestamp of when the conversation was last updated")

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
    messages: list[ConversationMessageResponse] = Field(
        default_factory=list, description="The messages of the conversation"
    )

    @classmethod
    def from_dto(cls, dto: Conversation) -> "ConversationWithMessagesResponse":
        return cls(
            **ConversationResponse.from_dto(dto=dto).model_dump(),
            messages=[ConversationMessageResponse.from_dto(dto=message) for message in dto.messages],
        )
