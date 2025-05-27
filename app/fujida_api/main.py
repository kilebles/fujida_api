import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.fujida_api.config import config
from app.fujida_api.routes import router as api_router

app = FastAPI(title='fujida_api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
    
)

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run(
        "fujida_api.main:app",
        host=config.APP_HOST,
        port=int(config.APP_PORT),
        reload=False
    )
