from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase


from dotenv import load_dotenv

from data.config import settin


load_dotenv()

async_engine = create_async_engine(
    url = settin.database_url_asyncpg,
    echo=True
    )

async_session = async_sessionmaker(async_engine, class_=AsyncSession)



class Base(DeclarativeBase):
    ...


async def async_main():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)