from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import DATABASE_URL, DEBUG

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=DEBUG, future=True)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
