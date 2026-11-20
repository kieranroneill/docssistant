from pydantic import Field

from libs.defaults.responses import BaseResponse


class VersionModelResponse(BaseResponse):
    chat: str = Field(description="The name of the chat model")
    embeddings: str = Field(description="The name of the embeddings model")


class VersionResponse(BaseResponse):
    description: str = Field(description="The description of the API")
    environment: str = Field(description="The environment of the API")
    models: VersionModelResponse = Field(description="The models")
    title: str = Field(description="The title of the API")
    version: str = Field(description="The version of the API")
