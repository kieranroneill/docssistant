from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from api.platform.defaults.repositories import BaseRepository

from .dtos import Conversation, ConversationMessage
from .models import ConversationMessageModel, ConversationModel


class ConversationMessageRepository(BaseRepository[ConversationMessageModel, ConversationMessage]):
    ##
    # private methods
    ##
    @property
    def _model_type(self) -> type[ConversationMessageModel]:
        return ConversationMessageModel

    def _to_model(self, dto: ConversationMessage) -> ConversationMessageModel:
        return dto.to_model()

    async def _to_dto(self, model: ConversationMessageModel) -> ConversationMessage:
        return ConversationMessage.from_model(model)

    ##
    # public methods
    ##
    async def add(self, dto: ConversationMessage) -> ConversationMessage:
        result = await super().add(dto)

        self._logger.debug('added "%s" entry: "%s"', ConversationMessageModel.__tablename__, result.id)

        return result

    async def bulk_add(self, dtos: list[ConversationMessage]) -> list[ConversationMessage]:
        results = await super().bulk_add(dtos)

        self._logger.debug(
            'added multiple "%s": %s',
            ConversationMessageModel.__tablename__,
            "[" + ", ".join(f'"{result.id}"' for result in results) + "]",
        )

        return results

    async def delete_by_id(self, _id: UUID) -> bool:
        result = await super().delete_by_id(_id)

        if result:
            self._logger.debug('deleted "%s" entry: "%s"', ConversationMessageModel, _id)

        return result

    async def update(
        self,
        dto: ConversationMessage,
    ) -> ConversationMessage | None:
        model = await self._postgres.get(self._model_type, dto.id)

        if model is None:
            return None

        model.content = dto.content
        model.input_tokens = dto.usage.input_tokens if dto.usage else None
        model.model = dto.model
        model.output_tokens = dto.usage.output_tokens if dto.usage else None
        model.role = dto.role
        model.sequence_number = dto.sequence_number
        model.total_tokens = dto.usage.total_tokens if dto.usage else None

        try:
            await self._postgres.commit()
            await self._postgres.refresh(model)
        except Exception:
            await self._postgres.rollback()
            raise

        self._logger.debug('updated "%s" entry: "%s"', ConversationMessageModel, model.id)

        return await self._to_dto(model)


class ConversationRepository(BaseRepository[ConversationModel, Conversation]):
    ##
    # private methods
    ##
    @property
    def _model_type(self) -> type[ConversationModel]:
        return ConversationModel

    def _to_model(self, dto: Conversation) -> ConversationModel:
        return dto.to_model()

    async def _to_dto(self, model: ConversationModel) -> Conversation:
        statement = select(ConversationModel).where(ConversationModel.id == model.id)
        result = await self._postgres.execute(statement)
        _model = result.scalar_one()

        return Conversation.from_model(_model)

    ##
    # public methods
    ##
    async def add(self, dto: Conversation) -> Conversation:
        result = await super().add(dto)

        self._logger.debug('added "%s" entry: "%s"', ConversationModel.__tablename__, result.id)

        return result

    async def bulk_add(self, dtos: list[Conversation]) -> list[Conversation]:
        results = await super().bulk_add(dtos)

        self._logger.debug(
            'added multiple "%s": %s',
            ConversationModel.__tablename__,
            "[" + ", ".join(f'"{result.id}"' for result in results) + "]",
        )

        return results

    async def delete_by_id(self, _id: UUID) -> bool:
        result = await super().delete_by_id(_id)

        if result:
            self._logger.debug('deleted "%s" entry: "%s"', ConversationModel, _id)

        return result

    async def get_by_id_with_messages(self, _id: UUID) -> Conversation | None:
        statement = (
            select(ConversationModel)
            .options(selectinload(ConversationModel.messages))
            .where(ConversationModel.id == _id)
        )
        result = await self._postgres.execute(statement)
        model = result.scalar_one_or_none()

        return Conversation.from_model(model) if model else None

    async def update(self, dto: Conversation) -> Conversation | None:
        model = await self._postgres.get(self._model_type, dto.id)

        if model is None:
            return None

        model.active = dto.active

        try:
            await self._postgres.commit()
            await self._postgres.refresh(model)
        except Exception:
            await self._postgres.rollback()
            raise

        self._logger.debug('updated "%s" entry: "%s"', ConversationModel, model.id)

        return await self._to_dto(model)
