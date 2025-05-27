import csv
import asyncio
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.fujida_api.db.models import DeviceModel, DeviceSpec
from app.fujida_api.db.session import async_session_maker

CSV_PATH = Path('actual.csv')


async def import_models():
    async with async_session_maker() as session:
        with CSV_PATH.open('r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                model_name = row.pop('model_name').strip()

                model = DeviceModel(name=model_name)
                session.add(model)
                await session.flush() 

                for spec_name, value in row.items():
                    spec = DeviceSpec(
                        model_id=model.id,
                        name=spec_name.strip(),
                        value=value.strip() if value else None
                    )
                    session.add(spec)

        await session.commit()
        print('✅ Import complete')


if __name__ == '__main__':
    asyncio.run(import_models())
