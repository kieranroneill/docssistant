from api.platform.defaults.dtos import BaseDTO


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
