import sys
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Adjust database URL if postgres isn't running or sqlite is specified
db_url = settings.DATABASE_URL
if "postgresql" in db_url and "asyncpg" not in db_url:
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")

# If initializing local SQLite, ensure correct async dialect
if db_url.startswith("sqlite"):
    if "sqlite+aiosqlite" not in db_url:
        db_url = db_url.replace("sqlite://", "sqlite+aiosqlite://")

engine = create_async_engine(
    db_url,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False} if "sqlite" in db_url else {}
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
