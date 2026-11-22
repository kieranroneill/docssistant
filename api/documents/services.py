from logging import Logger
from pathlib import Path
from uuid import UUID

from fastapi import status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from libs.defaults.services import BaseService
from libs.documents.repositories import DocumentVersionRepository

from .errors import DocumentNotFoundError


class Service(BaseService):
    _documents_path: Path
    _document_versions_repository: DocumentVersionRepository

    def __init__(
        self,
        documents_path: Path,
        logger: Logger,
        postgres_session: AsyncSession,
    ):
        super().__init__(logger=logger)

        self._documents_path = documents_path
        self._document_versions_repository = DocumentVersionRepository(logger=logger, postgres_session=postgres_session)

    ###
    # private methods
    ###

    ###
    # public methods
    ###

    async def document_by_id(
        self,
        document_id: UUID,
    ) -> FileResponse:
        document = await self._document_versions_repository.get_by_document_id(document_id=document_id)

        if document is None or document.active is False:
            raise DocumentNotFoundError(message=f"document '{str(document_id)}' not found").to_http_exception(
                status_code=status.HTTP_404_NOT_FOUND
            )

        self._logger.debug(f"document '{str(document_id)}' found")

        root = self._documents_path.resolve()
        path = (root / document.source).resolve()

        if not path.is_relative_to(root) or not path.is_file():
            raise DocumentNotFoundError(message=f"document '{str(document_id)}' not found").to_http_exception(
                status_code=status.HTTP_404_NOT_FOUND
            )

        is_pdf = path.suffix.lower() == ".pdf"

        return FileResponse(
            path=path,
            filename=Path(document.source).name,
            media_type="application/pdf" if is_pdf else "application/octet-stream",
            content_disposition_type="inline" if is_pdf else "attachment",
        )
