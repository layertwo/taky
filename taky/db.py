import logging
import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from taky.config import app_config

lgr = logging.getLogger(__name__)


def build_session_factory(url: str | None = None) -> async_sessionmaker[AsyncSession]:
    """Build an async session factory from the given URL or configured defaults.

    URL resolution order:
    1. Explicit ``url`` argument
    2. ``DATABASE_URL`` environment variable
    3. ``[db] url`` in taky.conf
    4. In-memory SQLite (fallback with warning)
    """
    if url is None:
        url = os.environ.get("DATABASE_URL")

    if url is None:
        url = app_config.get("db", "url", fallback=None)

    if url is None:
        lgr.warning("No database URL configured — DB operations will fail at runtime")
        url = "sqlite+aiosqlite:///:memory:"

    pool_kwargs: dict = {"pool_pre_ping": True}

    if url.startswith("sqlite"):
        from sqlalchemy.pool import StaticPool

        pool_kwargs["poolclass"] = StaticPool
        pool_kwargs["connect_args"] = {"check_same_thread": False}
    else:
        pool_kwargs["pool_size"] = 5
        pool_kwargs["max_overflow"] = 10

    engine = create_async_engine(url, **pool_kwargs)

    return async_sessionmaker(engine, expire_on_commit=False)


async def get_session(
    factory: async_sessionmaker[AsyncSession] | None = None,
) -> AsyncGenerator[AsyncSession, None]:
    """Async generator yielding a database session.

    If no factory is provided, one is built lazily from current configuration.
    """
    if factory is None:
        factory = build_session_factory()

    async with factory() as session:
        yield session
