from libs.defaults.responses import BaseResponse


class VersionModelResponse(BaseResponse):
    chat: str
    embeddings: str


class VersionResponse(BaseResponse):
    description: str
    environment: str
    models: VersionModelResponse
    title: str
    version: str
