import os
from logging import Logger

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class PostgresClient:
    _engine: AsyncEngine
    _logger: Logger

    def __init__(self, logger: Logger) -> None:
        # TODO: check if env vars are set
        self._engine = create_async_engine(
            pool_pre_ping=True,
            url=URL.create(
                drivername="postgresql+asyncpg",
                username=os.environ["POSTGRES_USER"],
                password=os.environ["POSTGRES_PASSWORD"],
                host=os.environ["POSTGRES_HOST"],
                port=int(os.environ["POSTGRES_PORT"]),
                database=os.environ["POSTGRES_DB"],
            ),
        )
        self._logger = logger

    def create_session(self) -> AsyncSession:
        return async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )()

    async def dispose(self):
        return await self._engine.dispose()
