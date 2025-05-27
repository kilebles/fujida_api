from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.fujida_api.config import config

engine = create_async_engine(config.DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)