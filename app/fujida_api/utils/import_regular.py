import csv
import asyncio
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.fujida_api.db.models import DeviceModel, DeviceSpec
from app.fujida_api.db.session import async_session_maker

CSV_PATH = Path('regular.csv')


def is_valid_column(column: str) -> bool:
    return not (column.startswith('Unnamed') or column.endswith('.1'))


def clean_value(value) -> str | None:
    if value is None:
        return None
    value_str = str(value).strip()
    return value_str if value_str and value_str.lower() != 'nan' else None


async def import_models():
    async with async_session_maker() as session:
        with CSV_PATH.open('r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                model_name = row.pop('model_name', '').strip()
                if not model_name:
                    continue

                result = await session.execute(
                    select(DeviceModel).where(DeviceModel.name == model_name)
                )
                existing = result.scalar_one_or_none()

                if existing:
                    print(f'Updating specs for: {model_name}')
                    model_id = existing.id

                    await session.execute(
                        delete(DeviceSpec).where(DeviceSpec.model_id == model_id)
                    )

                else:
                    model = DeviceModel(name=model_name)
                    session.add(model)
                    await session.flush()
                    model_id = model.id
                    print(f'Added new model: {model_name}')

                for spec_name, value in row.items():
                    if not is_valid_column(spec_name):
                        continue

                    cleaned_value = clean_value(value)
                    if cleaned_value is None:
                        continue

                    spec = DeviceSpec(
                        model_id=model_id,
                        name=spec_name.strip(),
                        value=cleaned_value
                    )
                    session.add(spec)

        await session.commit()


if __name__ == '__main__':
    asyncio.run(import_models())
