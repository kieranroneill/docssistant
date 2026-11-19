from pydantic import Field

from libs.defaults.dtos import BaseDTO


class ChatRequest(BaseDTO, frozen=True):
    query: str = Field(..., min_length=1)
