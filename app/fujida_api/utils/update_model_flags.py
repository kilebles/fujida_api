import asyncio

from sqlalchemy import select, update
from app.fujida_api.db.session import async_session_maker
from app.fujida_api.db.models import DeviceModel

ACTIVE_MODELS = [
    "Fujida Karma Pro Max Duo WiFi",
    "Fujida Karma Pro Max AI WiFi",
    "Fujida Karma Pro S WiFi",
    "Fujida Karma One",
    "Fujida Karma Hit",
    "Fujida Zoom Smart Max WiFi",
    "Fujida Zoom Smart S WiFi",
    "Fujida Zoom Hit S Duo WiFi",
    "Fujida Zoom Hit S WiFi",
    "Fujida Zoom Okko WiFi",
]

DETECTORS = [
    "Fujida Magna",
    "Fujida Era",
    "Fujida Global"
]


async def update_flags():
    async with async_session_maker() as session:
        result = await session.execute(select(DeviceModel))
        models = result.scalars().all()

        for model in models:
            model.is_active = model.name in ACTIVE_MODELS
            model.is_detector = model.name in DETECTORS

        await session.commit()
        print('✅ Flags updated successfully.')


if __name__ == '__main__':
    asyncio.run(update_flags())
