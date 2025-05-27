import asyncio
import logging

from sqlalchemy import select
from openai import AsyncOpenAI

from app.fujida_api.db.session import async_session_maker
from app.fujida_api.db.models import DeviceModel
from app.fujida_api.config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)


async def generate_embeddings():
    async with async_session_maker() as session:
        result = await session.execute(
            select(DeviceModel).where(DeviceModel.embedding.is_(None))
        )
        records = result.scalars().all()

        for record in records:
            try:
                response = await client.embeddings.create(
                    input=record.name.strip(),
                    model="text-embedding-3-small",
                    encoding_format="float"
                )
                record.embedding = response.data[0].embedding
                logger.info(f"Embedding generated for: {record.name}")
            except Exception as e:
                logger.error(f"Error generating for {record.name}: {e}")

        await session.commit()
        logger.info("All embeddings generated and saved!")


if __name__ == "__main__":
    asyncio.run(generate_embeddings())
