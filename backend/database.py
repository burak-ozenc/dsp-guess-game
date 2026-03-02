import ssl
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config.config import config

# Create SSL context for NeonDB
ssl_context = ssl.create_default_context()

# Build engine with SSL for asyncpg
engine = create_async_engine(
    config.DATABASE_URL,
    connect_args={"ssl": ssl_context}
)

# Session factory
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Declarative base
class Base(DeclarativeBase):
    pass


# Dependency for FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
