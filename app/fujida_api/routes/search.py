from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from sqlalchemy.orm import selectinload

from app.fujida_api.db.models import DeviceModel
from app.fujida_api.db.session import get_async_session
from app.fujida_api.schemas.search import DeviceSearchResult
from app.fujida_api.services.search_service import generate_query_embedding, get_similar_models

router = APIRouter()


@router.get("/search", response_model=list[DeviceSearchResult])
async def search_models(
    query: str = Query(..., description="Название или часть названия модели"),
    limit: int = Query(3, ge=1, le=10),
    session: AsyncSession = Depends(get_async_session),
):
    embedding = await generate_query_embedding(query)
    models = await get_similar_models(session, embedding, limit)
    return models
