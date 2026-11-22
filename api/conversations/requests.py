from pydantic import Field

from libs.defaults.requests import BaseRequest

from .constants import MAX_QUERY_LENGTH


class ChatRequest(BaseRequest):
    query: str = Field(
        description="The query to ask the assistant",
        max_length=MAX_QUERY_LENGTH,
        min_length=1,
    )
