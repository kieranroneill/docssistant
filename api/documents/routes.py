from logging import Logger
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from libs.logging.dependencies import get_logger
from libs.postgres.dependencies import get_session as get_postgres_session

from .dependencies import get_documents_path
from .services import Service

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)


@router.get(
    "/{document_id}",
    description="Gets the specified document",
    response_class=FileResponse,
    status_code=status.HTTP_200_OK,
)
async def document_by_id(
    document_id: UUID,
    documents_path: Path = Depends(get_documents_path),
    logger: Logger = Depends(get_logger),
    postgres_session: AsyncSession = Depends(get_postgres_session),
) -> FileResponse:
    service = Service(
        documents_path=documents_path,
        logger=logger,
        postgres_session=postgres_session,
    )

    return await service.document_by_id(document_id=document_id)
