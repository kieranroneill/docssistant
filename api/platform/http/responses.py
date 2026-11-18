from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorResponse:
    code: int
    message: str
