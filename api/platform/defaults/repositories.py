from abc import ABC, abstractmethod
from logging import Logger
from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

Model = TypeVar("Model")
DTO = TypeVar("DTO")


class BaseRepository(ABC, Generic[Model, DTO]):
    _logger: Logger
    _postgres: AsyncSession

    def __init__(self, postgres: AsyncSession, logger: Logger) -> None:
        self._logger = logger
        self._postgres = postgres

    ##
    # private methods
    ##
    @property
    @abstractmethod
    def _model_type(self) -> type[Model]:
        raise NotImplementedError

    @abstractmethod
    def _to_model(self, dto: DTO) -> Model:
        raise NotImplementedError

    @abstractmethod
    async def _to_dto(self, model: Model) -> DTO:
        raise NotImplementedError

    ##
    # public methods
    ##
    async def add(self, dto: DTO) -> DTO:
        model = self._to_model(dto)

        try:
            self._postgres.add(model)
            await self._postgres.commit()
            await self._postgres.refresh(model)
        except Exception:
            await self._postgres.rollback()
            raise

        return await self._to_dto(model)

    async def bulk_add(self, dtos: list[DTO]) -> list[DTO]:
        if not dtos:
            return []

        models = [self._to_model(dto) for dto in dtos]

        try:
            self._postgres.add_all(models)
            await self._postgres.commit()

            for model in models:
                await self._postgres.refresh(model)
        except Exception:
            await self._postgres.rollback()
            raise

        self._logger.debug(f'added multiple "{self._model_type}": [{[model.id for model in models]}]')

        return [await self._to_dto(model) for model in models]

    async def delete_by_id(self, _id: UUID) -> bool:
        model = await self._postgres.get(self._model_type, _id)

        if model is None:
            return False

        try:
            await self._postgres.delete(model)
            await self._postgres.commit()
        except Exception:
            await self._postgres.rollback()
            raise

        return True

    async def get_by_id(self, _id: UUID) -> DTO | None:
        model = await self._postgres.get(self._model_type, _id)

        if model is None:
            return None

        return await self._to_dto(model)
