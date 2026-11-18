from pydantic import Field

from api.platform.defaults.dtos import BaseDTO


class ChatRequest(BaseDTO, frozen=True):
    query: str = Field(..., min_length=1)
