from collections.abc import AsyncIterator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from .clients import PostgresClient


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    """
    Create a Postgres session for the active request lifecycle.

    Args:
        request (Request): The current FastAPI request.

    Returns:
        AsyncIterator[AsyncSession]: An asynchronous iterator yielding a database session for the request.
    """
    postgres: PostgresClient = request.app.state.postgres

    async with postgres.create_session() as session:
        yield session
