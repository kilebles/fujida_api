from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.fujida_api.db.session import get_async_session
from app.fujida_api.schemas.search import DeviceSearchResult
from app.fujida_api.services.compare_service import get_models_for_comparison

router = APIRouter()


@router.get('/compare', response_model=dict[str, DeviceSearchResult])
async def compare_models(
    models: list[str] = Query(..., min_items=2),
    session: AsyncSession = Depends(get_async_session),
):
    return await get_models_for_comparison(models, session)