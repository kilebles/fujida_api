import uvicorn
from fastapi import FastAPI

from app.fujida_api.config import config
from app.fujida_api.routes import router as api_router
from app.fujida_api.middlewares.admin_auth import AdminAuthMiddleware
from app.fujida_api.middlewares.cors import setup_cors
from app.fujida_api.admin.admin import setup_admin

app = FastAPI(title='fujida_api')

app.add_middleware(AdminAuthMiddleware)
setup_cors(app)

app.include_router(api_router)
setup_admin(app)

if __name__ == '__main__':
    uvicorn.run(
        'fujida_api.main:app',
        host=config.APP_HOST,
        port=int(config.APP_PORT),
        reload=False
    )
