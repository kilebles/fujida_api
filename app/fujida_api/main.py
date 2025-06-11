import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqladmin import Admin, ModelView

from app.fujida_api.config import config
from app.fujida_api.routes import router as api_router

from app.fujida_api.db.models import FAQEntry

SYNC_DATABASE_URL = config.DATABASE_URL.replace('postgresql+asyncpg', 'postgresql')

sync_engine = create_engine(SYNC_DATABASE_URL, echo=False)  # под Админку синхронный

app = FastAPI(title='fujida_api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
    
)

app.include_router(api_router)
admin = Admin(app, sync_engine)

class FAQEntryAdmin(ModelView, model=FAQEntry):
    column_list = [FAQEntry.id, FAQEntry.question, FAQEntry.answer]
    form_columns = ['question', 'answer']

admin.add_view(FAQEntryAdmin)

if __name__ == '__main__':
    uvicorn.run(
        "fujida_api.main:app",
        host=config.APP_HOST,
        port=int(config.APP_PORT),
        reload=False
    )
