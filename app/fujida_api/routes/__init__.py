from fastapi import APIRouter

from app.fujida_api.routes import search
from app.fujida_api.routes import compare
from app.fujida_api.routes import faq

router = APIRouter()
     
router.include_router(search.router)
router.include_router(compare.router)
router.include_router(faq.router)