from sqlalchemy.ext.asyncio import AsyncSession
from app.fujida_api.services.search_service import generate_query_embedding, get_similar_models
from app.fujida_api.schemas.search import DeviceSearchResult


async def get_models_for_comparison(
    model_names: list[str],
    session: AsyncSession,
) -> dict[str, DeviceSearchResult]:
    result: dict[str, DeviceSearchResult] = {}

    for name in model_names:
        embedding = await generate_query_embedding(name)
        models = await get_similar_models(session, embedding, limit=1)
        if models:
            result[name] = models[0]

    return result
