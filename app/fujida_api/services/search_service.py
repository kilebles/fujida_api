from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from sqlalchemy.orm import selectinload
from openai import AsyncOpenAI

from app.fujida_api.db.models import DeviceModel
from app.fujida_api.schemas.search import DeviceSearchResult, DeviceSpecOut
from app.fujida_api.config import config

openai_client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)

async def generate_query_embedding(query: str) -> list[float]:
    response = await openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    return response.data[0].embedding

async def get_similar_models(session: AsyncSession, query_vector: list[float], limit: int) -> list[DeviceSearchResult]:
    stmt = (
        select(DeviceModel)
        .where(DeviceModel.embedding.is_not(None))
        .order_by(DeviceModel.embedding.l2_distance(query_vector))
        .limit(limit)
        .options(selectinload(DeviceModel.specs))
    )
    result = await session.execute(stmt)
    models = result.scalars().all()

    return [
        DeviceSearchResult(
            id=m.id,
            name=m.name,
            specs=[DeviceSpecOut(name=s.name, value=s.value) for s in m.specs]
        )
        for m in models
    ]
