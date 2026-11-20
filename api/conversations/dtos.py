from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from sqlalchemy import inspect

from .models import ConversationMessageModel, ConversationModel, ConversationSourceModel


@dataclass()
class Usage:
    input_tokens: int
    output_tokens: int
    total_tokens: int


@dataclass()
class ConversationSource:
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


@dataclass()
class ConversationMessage:
    created_at: datetime
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
            created_at=model.created_at,
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
            created_at=self.created_at,
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


@dataclass()
class Conversation:
    active: bool
    created_at: datetime
    id: UUID
    messages: list[ConversationMessage]
    title: str
    updated_at: datetime

    @classmethod
    def from_model(cls, model: ConversationModel) -> "Conversation":
        messages = (
            []
            if "messages" in inspect(model).unloaded
            else [ConversationMessage.from_model(message) for message in model.messages]
        )

        return cls(
            created_at=model.created_at,
            active=model.active,
            id=model.id,
            messages=messages,
            title=model.title,
            updated_at=model.updated_at,
        )

    def to_model(self) -> ConversationModel:
        return ConversationModel(
            active=self.active,
            created_at=self.created_at,
            id=self.id,
            messages=[message.to_model() for message in self.messages] if self.messages is not None else [],
            title=self.title,
            updated_at=self.updated_at,
        )
