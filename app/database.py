import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

DATABASE_URL = os.getenv(
    "BLOCKSEMBLER_DB_URI",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/blocksembler"
)

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
