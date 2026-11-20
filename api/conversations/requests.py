from pydantic import Field

from libs.defaults.requests import BaseRequest


class ChatRequest(BaseRequest):
    query: str = Field(..., min_length=1)
