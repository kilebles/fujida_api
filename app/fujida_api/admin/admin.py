from sqlalchemy import create_engine
from sqladmin import Admin, ModelView

from app.fujida_api.config import config
from app.fujida_api.db.models import FAQEntry

SYNC_DATABASE_URL = config.DATABASE_URL.replace('postgresql+asyncpg', 'postgresql')

sync_engine = create_engine(SYNC_DATABASE_URL, echo=False)


def setup_admin(app):
    admin = Admin(app, sync_engine)

    class FAQEntryAdmin(ModelView, model=FAQEntry):
        column_list = [FAQEntry.id, FAQEntry.question, FAQEntry.answer]
        form_columns = ['question', 'answer']

    admin.add_view(FAQEntryAdmin)
