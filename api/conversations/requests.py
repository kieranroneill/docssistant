from pydantic import Field

from libs.defaults.requests import BaseRequest


class ChatRequest(BaseRequest):
    query: str = Field(description="The query to ask the assistant", min_length=1)
