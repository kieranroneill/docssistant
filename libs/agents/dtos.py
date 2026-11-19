from libs.defaults.dtos import BaseDTO


class ChatMessage(BaseDTO, frozen=True):
    content: str
    role: str


class ChatResult(BaseDTO, frozen=True):
    content: str
    created_at: str
    input_tokens: int
    model: str
    output_tokens: int
    role: str
    total_tokens: int
