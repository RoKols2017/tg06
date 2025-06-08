from app.db.models import Base
from app.db.session import engine

import asyncio

"""
Создание всех таблиц БД. Запускать отдельно: `python -m app.create_tables`
"""

async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_all())