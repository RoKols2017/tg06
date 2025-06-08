"""
Создание асинхронного SQLAlchemy engine и sessionmaker.
"""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from contextlib import asynccontextmanager
from app.config import get_settings

settings = get_settings()
engine = create_async_engine(settings.database_url, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

@asynccontextmanager
async def new_session():
    """Контекст-менеджер для выдачи сессии в хэндлерах."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:  # pragma: no cover
            await session.rollback()
            raise
