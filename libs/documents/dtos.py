from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .models import DocumentVersionModel


@dataclass()
class DocumentChunk:
    content: str
    page_number: int | None = None


@dataclass()
class DocumentMatch:
    chunk_index: int
    content: str
    distance: float
    document_id: str
    source: str = ""
    page_number: int | None = None


@dataclass()
class DocumentVersion:
    active: bool
    created_at: datetime
    document_id: UUID
    id: UUID
    source: str
    updated_at: datetime
    version: str

    @classmethod
    def from_model(cls, model: DocumentVersionModel) -> "DocumentVersion":
        return cls(
            active=model.active,
            created_at=model.created_at,
            document_id=model.document_id,
            id=model.id,
            source=model.source,
            updated_at=model.updated_at,
            version=model.version,
        )

    def to_model(self) -> DocumentVersionModel:
        return DocumentVersionModel(
            active=self.active,
            created_at=self.created_at,
            document_id=self.document_id,
            id=self.id,
            source=self.source,
            updated_at=self.updated_at,
            version=self.version,
        )
