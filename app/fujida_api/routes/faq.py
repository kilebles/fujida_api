from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.fujida_api.db.session import get_async_session
from app.fujida_api.schemas.faq import FAQQuery, FAQAnswer
from app.fujida_api.services.faq_service import get_similar_faq

router = APIRouter()


@router.post('/faq/search', response_model=list[FAQAnswer])
async def faq_search(
    body: FAQQuery,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_similar_faq(body.query, session)
