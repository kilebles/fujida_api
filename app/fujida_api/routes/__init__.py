from fastapi import APIRouter

from app.fujida_api.routes import search

router = APIRouter()

router.include_router(search.router)