from uuid import UUID

from libs.datetime.utilities import from_iso_string, to_iso_string
from libs.defaults.dtos import BaseDTO

from .models import DocumentVersionModel


class DocumentChunk(BaseDTO):
    content: str
    page_number: int | None = None


class DocumentMatch(BaseDTO):
    chunk_index: int
    content: str
    distance: float
    document_id: str
    source: str = ""
    page_number: int | None = None


class DocumentVersion(BaseDTO):
    active: bool
    created_at: str
    document_id: UUID
    id: UUID
    source: str
    updated_at: str
    version: str

    @classmethod
    def from_model(cls, model: DocumentVersionModel) -> "DocumentVersion":
        return cls(
            active=model.active,
            created_at=to_iso_string(model.created_at),
            document_id=model.document_id,
            id=model.id,
            source=model.source,
            updated_at=to_iso_string(model.updated_at),
            version=model.version,
        )

    def to_model(self) -> DocumentVersionModel:
        return DocumentVersionModel(
            active=self.active,
            created_at=from_iso_string(self.created_at),
            document_id=self.document_id,
            id=self.id,
            source=self.source,
            updated_at=from_iso_string(self.updated_at),
            version=self.version,
        )
