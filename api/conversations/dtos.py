from uuid import UUID

from sqlalchemy import inspect

from libs.datetime.utilities import from_iso_string, to_iso_string
from libs.defaults.dtos import BaseDTO

from .models import ConversationMessageModel, ConversationModel, ConversationSourceModel


class Usage(BaseDTO):
    input_tokens: int
    output_tokens: int
    total_tokens: int


class ConversationSource(BaseDTO):
    chunk_index: int
    document_id: UUID
    id: UUID
    page_number: int | None
    reference: int
    source: str

    @classmethod
    def from_model(cls, model: ConversationSourceModel) -> "ConversationSource":
        return cls(
            chunk_index=model.chunk_index,
            document_id=model.document_id,
            id=model.id,
            page_number=model.page_number,
            reference=model.reference,
            source=model.source,
        )

    def to_model(self) -> ConversationSourceModel:
        return ConversationSourceModel(
            chunk_index=self.chunk_index,
            document_id=self.document_id,
            id=self.id,
            page_number=self.page_number,
            reference=self.reference,
            source=self.source,
        )


class ConversationMessage(BaseDTO):
    created_at: str
    content: str
    conversation_id: UUID
    id: UUID
    model: str | None
    role: str
    sequence_number: int
    sources: list[ConversationSource]
    usage: Usage | None

    @classmethod
    def from_model(cls, model: ConversationMessageModel) -> "ConversationMessage":
        sources = (
            []
            if "sources" in inspect(model).unloaded
            else [ConversationSource.from_model(source) for source in model.sources]
        )
        usage: Usage | None = None

        if model.input_tokens and model.output_tokens and model.total_tokens:
            usage = Usage(
                input_tokens=model.input_tokens,
                output_tokens=model.output_tokens,
                total_tokens=model.total_tokens,
            )

        return cls(
            created_at=to_iso_string(model.created_at),
            content=model.content,
            conversation_id=model.conversation_id,
            id=model.id,
            model=model.model,
            role=model.role,
            sequence_number=model.sequence_number,
            sources=sources,
            usage=usage,
        )

    def to_model(self) -> ConversationMessageModel:
        return ConversationMessageModel(
            created_at=from_iso_string(self.created_at),
            content=self.content,
            conversation_id=self.conversation_id,
            id=self.id,
            input_tokens=self.usage.input_tokens if self.usage else None,
            model=self.model,
            output_tokens=self.usage.output_tokens if self.usage else None,
            role=self.role,
            sequence_number=self.sequence_number,
            sources=[source.to_model() for source in self.sources],
            total_tokens=self.usage.total_tokens if self.usage else None,
        )


class Conversation(BaseDTO):
    active: bool
    created_at: str
    id: UUID
    messages: list[ConversationMessage]
    updated_at: str

    @classmethod
    def from_model(cls, model: ConversationModel) -> "Conversation":
        messages = (
            []
            if "messages" in inspect(model).unloaded
            else [ConversationMessage.from_model(message) for message in model.messages]
        )

        return cls(
            created_at=to_iso_string(model.created_at),
            active=model.active,
            id=model.id,
            messages=messages,
            updated_at=to_iso_string(model.updated_at),
        )

    def to_model(self) -> ConversationModel:
        return ConversationModel(
            active=self.active,
            created_at=from_iso_string(self.created_at),
            id=self.id,
            messages=[message.to_model() for message in self.messages] if self.messages is not None else [],
            updated_at=from_iso_string(self.updated_at),
        )
