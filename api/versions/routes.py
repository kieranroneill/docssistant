from fastapi import APIRouter, Depends, Response, status

from libs.agents.clients import ChatAgent, EmbeddingsAgent
from libs.agents.dependencies import get_chat_agent, get_embeddings_agent
from libs.application.dependencies import get_application
from libs.application.dtos import Application

from .responses import VersionModelResponse, VersionResponse

router = APIRouter(
    prefix="/api/versions",
    tags=["versions"],
)


@router.get(
    "",
    description="Gets information about the API",
    response_model=VersionResponse,
    status_code=status.HTTP_200_OK,
)
async def versions(
    response: Response,
    chat_agent: ChatAgent = Depends(get_chat_agent),
    embeddings_agent: EmbeddingsAgent = Depends(get_embeddings_agent),
    application: Application = Depends(get_application),
) -> VersionResponse:
    response.status_code = status.HTTP_200_OK

    return VersionResponse(
        description=application.description,
        environment=application.environment,
        models=VersionModelResponse(
            chat=chat_agent.model(),
            embeddings=embeddings_agent.model(),
        ),
        title=application.title,
        version=application.version,
    )
