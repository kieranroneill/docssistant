from api.platform.defaults.dtos import BaseDTO


class Usage(BaseDTO):
    input_tokens: int
    output_tokens: int
    total_tokens: int


class ChatResult(BaseDTO):
    created_at: str
    content: str
    model: str
    role: str
    usage: Usage


class Message(BaseDTO):
    content: str
    role: str
