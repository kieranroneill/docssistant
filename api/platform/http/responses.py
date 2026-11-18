from api.platform.defaults.dtos import BaseDTO


class ErrorResponse(BaseDTO):
    code: int
    message: str
