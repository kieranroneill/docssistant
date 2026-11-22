from asyncio import Event
from logging import Logger
from pathlib import Path
from test.mocks.agents.clients import MockEmbeddingsAgent

import pytest
from chromadb import GetResult
from chromadb.api.models.AsyncCollection import AsyncCollection
from chromadb.api.types import Where
from sqlalchemy.ext.asyncio import AsyncSession

from indexer.services import IndexerService
from libs.documents.errors import DocumentPathDoesNotExistError
from libs.documents.repositories import DocumentVersionRepository


@pytest.fixture
def document_version_repository(
    logger: Logger,
    postgres_session: AsyncSession,
) -> DocumentVersionRepository:
    return DocumentVersionRepository(logger=logger, postgres_session=postgres_session)


@pytest.fixture
def service(
    chroma_collection: AsyncCollection,
    embeddings_agent: MockEmbeddingsAgent,
    logger: Logger,
    postgres_session: AsyncSession,
) -> IndexerService:
    return IndexerService(
        chroma_collection=chroma_collection,
        embeddings_agent=embeddings_agent,
        logger=logger,
        postgres_session=postgres_session,
    )


async def chunks_for(collection: AsyncCollection, source: str) -> GetResult:
    where: Where = {"document_id": str(IndexerService.document_id_from_source(source=source))}

    return await collection.get(include=["documents", "metadatas"], where=where)


class TestIndex:
    async def test_should_fail_if_the_documents_path_does_not_exist(
        self,
        documents_path: Path,
        service: IndexerService,
    ) -> None:
        with pytest.raises(DocumentPathDoesNotExistError):
            await service.index(documents_path=documents_path / "does-not-exist")

    async def test_should_index_nothing_for_an_empty_documents_path(
        self,
        service: IndexerService,
        temp_documents_path: Path,
    ) -> None:
        # git cannot track an empty directory, so this one case needs a directory of its own
        assert await service.index(documents_path=temp_documents_path) == 0

    async def test_should_index_a_text_document(
        self,
        chroma_collection: AsyncCollection,
        document_version_repository: DocumentVersionRepository,
        documents_path: Path,
        service: IndexerService,
    ) -> None:
        source = "handbook.md"

        indexed = await service.index(documents_path=documents_path / "text")

        assert indexed == 1

        # the chunk should be searchable in chroma, carrying the source and version metadata
        result = await chunks_for(collection=chroma_collection, source=source)

        assert result["documents"] == ["The office opens at 9am."]

        metadata = (result["metadatas"] or [])[0]

        assert metadata["chunk_index"] == 0
        assert metadata["source"] == source
        assert metadata.get("page_number") is None

        # the version should be published and active
        active_versions = await document_version_repository.get_all_active()

        assert len(active_versions) == 1
        assert active_versions[0].document_id == IndexerService.document_id_from_source(source=source)
        assert active_versions[0].source == source
        assert active_versions[0].version == metadata["version"]

    async def test_should_index_a_pdf_document_with_page_numbers(
        self,
        chroma_collection: AsyncCollection,
        documents_path: Path,
        service: IndexerService,
    ) -> None:
        indexed = await service.index(documents_path=documents_path / "pdf")

        assert indexed == 1

        # the fixture has one line of text per page, so each page yields exactly one chunk
        result = await chunks_for(collection=chroma_collection, source="report.pdf")
        page_numbers = sorted(int(str(metadata["page_number"])) for metadata in (result["metadatas"] or []))

        assert len(result["ids"]) == 2
        assert page_numbers == [1, 2]
        assert any("first quarter" in str(content) for content in (result["documents"] or []))
        assert any("second quarter" in str(content) for content in (result["documents"] or []))

    async def test_should_ignore_a_pdf_document_with_no_extractable_text(
        self,
        document_version_repository: DocumentVersionRepository,
        documents_path: Path,
        service: IndexerService,
    ) -> None:
        # a scanned pdf has pages, but no text layer to extract
        assert await service.index(documents_path=documents_path / "scanned") == 0
        assert await document_version_repository.get_all_active() == []

    async def test_should_index_a_nested_document_using_a_posix_source(
        self,
        document_version_repository: DocumentVersionRepository,
        documents_path: Path,
        service: IndexerService,
    ) -> None:
        assert await service.index(documents_path=documents_path / "nested") == 1

        active_versions = await document_version_repository.get_all_active()

        assert len(active_versions) == 1
        assert active_versions[0].source == "policies/leave/annual.txt"

    async def test_should_split_a_large_document_into_overlapping_chunks(
        self,
        chroma_collection: AsyncCollection,
        documents_path: Path,
        service: IndexerService,
    ) -> None:
        # the fixture is comfortably longer than the splitter's 1500 character chunk size
        assert await service.index(documents_path=documents_path / "large") == 1

        result = await chunks_for(collection=chroma_collection, source="large.txt")
        chunk_indexes = sorted(int(str(metadata["chunk_index"])) for metadata in (result["metadatas"] or []))

        assert len(chunk_indexes) > 1
        assert chunk_indexes == list(range(len(chunk_indexes)))

    async def test_should_ignore_unsupported_documents(
        self,
        document_version_repository: DocumentVersionRepository,
        documents_path: Path,
        service: IndexerService,
    ) -> None:
        assert await service.index(documents_path=documents_path / "unsupported") == 0
        assert await document_version_repository.get_all_active() == []

    async def test_should_ignore_a_document_with_no_extractable_text(
        self,
        document_version_repository: DocumentVersionRepository,
        documents_path: Path,
        service: IndexerService,
    ) -> None:
        assert await service.index(documents_path=documents_path / "empty") == 0
        assert await document_version_repository.get_all_active() == []

    async def test_should_ignore_a_symlink_pointing_outside_the_documents_path(
        self,
        document_version_repository: DocumentVersionRepository,
        documents_path: Path,
        service: IndexerService,
    ) -> None:
        # the fixture is a symlink to 'test/fixtures/outside', which sits outside the documents directory
        assert await service.index(documents_path=documents_path / "symlink") == 0
        assert await document_version_repository.get_all_active() == []

    async def test_should_keep_indexing_after_a_document_fails(
        self,
        document_version_repository: DocumentVersionRepository,
        documents_path: Path,
        mocker,
        service: IndexerService,
    ) -> None:
        read_text = Path.read_text

        def fail_for_broken(self: Path, *args, **kwargs) -> str:
            if self.name == "broken.md":
                raise OSError("could not read document")

            return read_text(self, *args, **kwargs)

        mocker.patch.object(Path, "read_text", fail_for_broken)

        assert await service.index(documents_path=documents_path / "multiple") == 1

        active_versions = await document_version_repository.get_all_active()

        assert [version.source for version in active_versions] == ["handbook.md"]

    async def test_should_not_publish_a_version_when_the_embedding_count_is_wrong(
        self,
        chroma_collection: AsyncCollection,
        document_version_repository: DocumentVersionRepository,
        documents_path: Path,
        logger: Logger,
        postgres_session: AsyncSession,
    ) -> None:
        # the agent returns a single embedding regardless of how many chunks it is given
        service = IndexerService(
            chroma_collection=chroma_collection,
            embeddings_agent=MockEmbeddingsAgent(documents_response=[[1.0, 0.0]], logger=logger),
            logger=logger,
            postgres_session=postgres_session,
        )

        assert await service.index(documents_path=documents_path / "large") == 0
        assert await document_version_repository.get_all_active() == []

    async def test_should_not_reindex_an_unchanged_document(
        self,
        document_version_repository: DocumentVersionRepository,
        documents_path: Path,
        service: IndexerService,
    ) -> None:
        assert await service.index(documents_path=documents_path / "text") == 1

        first_pass = await document_version_repository.get_all_active()

        # a second pass over identical content is a no-op
        assert await service.index(documents_path=documents_path / "text") == 0

        second_pass = await document_version_repository.get_all_active()

        assert [version.version for version in second_pass] == [version.version for version in first_pass]

    async def test_should_publish_a_new_version_when_a_document_changes(
        self,
        chroma_collection: AsyncCollection,
        document_version_repository: DocumentVersionRepository,
        service: IndexerService,
        temp_documents_path: Path,
    ) -> None:
        source = "handbook.md"
        path = temp_documents_path / source

        path.write_text("The office opens at 9am.", encoding="utf-8")

        await service.index(documents_path=temp_documents_path)

        original_version = (await document_version_repository.get_all_active())[0].version

        path.write_text("The office opens at 8am.", encoding="utf-8")

        assert await service.index(documents_path=temp_documents_path) == 1

        active_versions = await document_version_repository.get_all_active()

        # exactly one version stays active, and it is the new one
        assert len(active_versions) == 1
        assert active_versions[0].version != original_version

        # both versions' chunks remain in chroma, so search must filter by the active version
        result = await chunks_for(collection=chroma_collection, source=source)
        versions = {str(metadata["version"]) for metadata in (result["metadatas"] or [])}

        assert versions == {original_version, active_versions[0].version}

    async def test_should_reactivate_a_previous_version_when_a_document_reverts(
        self,
        document_version_repository: DocumentVersionRepository,
        service: IndexerService,
        temp_documents_path: Path,
    ) -> None:
        path = temp_documents_path / "handbook.md"
        original_content = "The office opens at 9am."

        path.write_text(original_content, encoding="utf-8")

        await service.index(documents_path=temp_documents_path)

        original_version = (await document_version_repository.get_all_active())[0].version

        path.write_text("The office opens at 8am.", encoding="utf-8")

        await service.index(documents_path=temp_documents_path)

        # revert the document: its chunks are already in chroma, so it is reactivated rather than re-embedded
        path.write_text(original_content, encoding="utf-8")

        assert await service.index(documents_path=temp_documents_path) == 1

        active_versions = await document_version_repository.get_all_active()

        assert len(active_versions) == 1
        assert active_versions[0].version == original_version

    async def test_should_deactivate_a_removed_document(
        self,
        document_version_repository: DocumentVersionRepository,
        service: IndexerService,
        temp_documents_path: Path,
    ) -> None:
        source = "handbook.md"
        path = temp_documents_path / source

        path.write_text("The office opens at 9am.", encoding="utf-8")

        await service.index(documents_path=temp_documents_path)

        assert len(await document_version_repository.get_all_active()) == 1

        path.unlink()

        assert await service.index(documents_path=temp_documents_path) == 0
        assert await document_version_repository.get_all_active() == []

        # the version row is kept, just deactivated
        version = await document_version_repository.get_by_document_id(
            document_id=IndexerService.document_id_from_source(source=source),
        )

        assert version is not None
        assert version.active is False

    async def test_should_keep_other_documents_active_when_one_is_removed(
        self,
        document_version_repository: DocumentVersionRepository,
        service: IndexerService,
        temp_documents_path: Path,
    ) -> None:
        (temp_documents_path / "handbook.md").write_text("The office opens at 9am.", encoding="utf-8")
        (temp_documents_path / "policies.txt").write_text("Expenses are reimbursed monthly.", encoding="utf-8")

        assert await service.index(documents_path=temp_documents_path) == 2

        (temp_documents_path / "handbook.md").unlink()

        await service.index(documents_path=temp_documents_path)

        active_versions = await document_version_repository.get_all_active()

        assert [version.source for version in active_versions] == ["policies.txt"]

    async def test_should_index_nothing_when_already_shutting_down(
        self,
        document_version_repository: DocumentVersionRepository,
        documents_path: Path,
        service: IndexerService,
    ) -> None:
        stop_event = Event()

        stop_event.set()

        assert await service.index(documents_path=documents_path / "multiple", stop_event=stop_event) == 0
        assert await document_version_repository.get_all_active() == []

    async def test_should_stop_between_documents_when_shutting_down(
        self,
        document_version_repository: DocumentVersionRepository,
        service: IndexerService,
        temp_documents_path: Path,
    ) -> None:
        stop_event = Event()

        (temp_documents_path / "a-handbook.md").write_text("The office opens at 9am.", encoding="utf-8")
        (temp_documents_path / "b-policies.txt").write_text("Expenses are reimbursed monthly.", encoding="utf-8")

        # stop once the first document has been published, so the pass ends with one document indexed, not two
        original_index_file = service._index_file

        async def index_file_then_stop(documents_path: Path, path: Path) -> bool:
            result = await original_index_file(documents_path=documents_path, path=path)

            stop_event.set()

            return result

        setattr(service, "_index_file", index_file_then_stop)

        assert await service.index(documents_path=temp_documents_path, stop_event=stop_event) == 1

        active_versions = await document_version_repository.get_all_active()

        # the published version is complete, and the document that was never reached has no version at all
        assert [version.source for version in active_versions] == ["a-handbook.md"]

    async def test_should_not_deactivate_removed_documents_when_shutting_down(
        self,
        document_version_repository: DocumentVersionRepository,
        service: IndexerService,
        temp_documents_path: Path,
    ) -> None:
        stop_event = Event()

        (temp_documents_path / "handbook.md").write_text("The office opens at 9am.", encoding="utf-8")

        assert await service.index(documents_path=temp_documents_path) == 1

        (temp_documents_path / "handbook.md").unlink()

        stop_event.set()

        await service.index(documents_path=temp_documents_path, stop_event=stop_event)

        active_versions = await document_version_repository.get_all_active()

        # deactivation is deferred to the next pass rather than half-done during shutdown
        assert [version.source for version in active_versions] == ["handbook.md"]
