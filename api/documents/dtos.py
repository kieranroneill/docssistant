from api.platform.defaults.dtos import BaseDTO


class DocumentMatch(BaseDTO):
    chunk_index: int
    content: str
    distance: float
    document_id: str
