import asyncio
import logging
from sqlalchemy import select
from openai import AsyncOpenAI

from app.fujida_api.db.session import async_session_maker
from app.fujida_api.db.models import FAQEntry
from app.fujida_api.config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)

MODEL_NAME = 'text-embedding-3-small'
BATCH_SIZE = 100


async def generate_faq_embeddings():
    async with async_session_maker() as session:
        result = await session.execute(
            select(FAQEntry).where(FAQEntry.embedding.is_(None))
        )
        records = result.scalars().all()

        if not records:
            logger.info("Нет записей для генерации эмбеддингов.")
            return

        logger.info(f"Найдено записей без эмбеддингов: {len(records)}")

        for i in range(0, len(records), BATCH_SIZE):
            batch = records[i:i + BATCH_SIZE]
            texts = [
                f'{entry.question.strip()}\n{entry.answer.strip()}'
                for entry in batch
            ]

            try:
                response = await client.embeddings.create(
                    input=texts,
                    model=MODEL_NAME,
                    encoding_format="float"
                )
                for record, item in zip(batch, response.data):
                    record.embedding = item.embedding

                logger.info(f"Обработано {len(batch)} записей (ID: {batch[0].id} – {batch[-1].id})")
            except Exception as e:
                logger.error(f"Ошибка при генерации эмбеддингов (ID {batch[0].id}): {e}")

        await session.commit()
        logger.info("Эмбеддинги FAQ успешно сгенерированы и сохранены.")


if __name__ == '__main__':
    asyncio.run(generate_faq_embeddings())
