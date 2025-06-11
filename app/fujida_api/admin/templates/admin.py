from sqlalchemy import create_engine
from sqladmin import Admin, ModelView, action

from app.fujida_api.config import config
from app.fujida_api.db.models import FAQEntry
from app.fujida_api.utils.generate_faq_embeddings import generate_embedding_for_text

SYNC_DATABASE_URL = config.DATABASE_URL.replace('postgresql+asyncpg', 'postgresql')

sync_engine = create_engine(SYNC_DATABASE_URL, echo=False)


def setup_admin(app):
    admin = Admin(app, sync_engine, templates_dir='app/fujida_api/admin/templates')

    class FAQEntryAdmin(ModelView, model=FAQEntry):
        column_list = [FAQEntry.id, FAQEntry.question, FAQEntry.answer]
        form_columns = ['question', 'answer']

        @action(
            name="regenerate_embeddings",
            text="Перегенерировать эмбеддинги"
        )
        async def regenerate_embeddings(self, request, entries):
            for entry in entries:
                text = f'{entry.question.strip()}\n{entry.answer.strip()}'
                try:
                    response = await generate_embedding_for_text(text)
                    entry.embedding = response
                except Exception as e:
                    print(f"Ошибка при генерации эмбеддинга для ID {entry.id}: {e}")

            await self.session.commit()


    admin.add_view(FAQEntryAdmin)
